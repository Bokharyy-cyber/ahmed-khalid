from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pathlib import Path
import os
import secrets
from sqlalchemy.orm import Session
from datetime import datetime

import models
import schemas
import email_service
from database import SessionLocal, engine

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "myweb"
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "").strip()
_allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")
ALLOWED_ORIGINS = [origin.strip() for origin in _allowed_origins if origin.strip()]

# ── Create all tables on startup
models.Base.metadata.create_all(bind=engine)

# ── Rate Limiter ✅ منع spam والهجمات
limiter = Limiter(key_func=get_remote_address)

# ── App instance
app = FastAPI(
    title="BOKHARY Portfolio API",
    description="Backend for Ahmed Khalid Gharib's personal portfolio",
    version="1.0.0"
)

# ── تسجيل limiter مع الـ app
app.state.limiter = limiter


# ✅ Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    أضف رؤوس الأمان المهمة:
    - X-Content-Type-Options: منع MIME type sniffing
    - X-Frame-Options: منع clickjacking
    - X-XSS-Protection: حماية من XSS (تصفح قديمة)
    - Content-Security-Policy: منع XSS والهجمات الأخرى
    - Strict-Transport-Security: فرض HTTPS
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # منع تحديد نوع MIME من قبل المتصفح
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # منع iframe embedding
        response.headers["X-Frame-Options"] = "DENY"
        
        # حماية من XSS (تصفح قديمة)
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # CSP - Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        
        # فرض HTTPS (في production)
        if os.getenv("ENVIRONMENT") == "production":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )
        
        # منع cache للبيانات الحساسة
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        
        return response


# ── CORS configuration ✅ محدود على الضروري فقط
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],  # ✅ فقط الضروري
    allow_headers=["Content-Type"],            # ✅ فقط الضروري
)

# ── Security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# ── Exception handler for rate limit
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return HTTPException(
        status_code=429,
        detail="Too many requests. Please try again later."
    )


# ── DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_admin_key(x_admin_key: str | None = Header(default=None, alias="X-Admin-Key")):
    """
    ✅ تحقق من وجود مفتاح API للإدارة
    يفشل بأمان إذا لم يكن المفتاح محدداً
    """
    # إذا لم يكن ADMIN_API_KEY محدداً، رفض الوصول
    if not ADMIN_API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Admin API is not configured. Please set ADMIN_API_KEY environment variable."
        )
    
    # تحقق من وجود مفتاح صحيح
    if not x_admin_key or not secrets.compare_digest(x_admin_key, ADMIN_API_KEY):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing admin key"
        )


# ══════════════════════════════════════════
#  ROUTES
# ══════════════════════════════════════════

@app.get("/api/health", tags=["Health"])
@app.get("/health", include_in_schema=False)
def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "project": "BOKHARY Portfolio API",
        "version": "1.0.0"
    }


@app.post(
    "/api/contact",
    response_model=schemas.ContactResponse,
    status_code=201,
    tags=["Contact"]
)
@app.post(
    "/contact",
    response_model=schemas.ContactResponse,
    status_code=201,
    include_in_schema=False
)
@limiter.limit("5/minute")  # ✅ 5 رسائل كل دقيقة لكل IP
async def submit_contact(
    request: Request,  # ← مطلوب للـ rate limiter
    payload: schemas.ContactCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Receive a contact form submission.
    - Saves the message to the database.
    - Sends an email notification in the background.
    
    ✅ محمي بـ rate limiting (5 رسائل/دقيقة)
    """

    # 1️⃣  Persist to database
    db_msg = models.Message(
        name     = payload.name.strip(),
        email    = payload.email.strip().lower(),
        subject  = payload.subject.strip(),
        message  = payload.message.strip(),
        sent_at  = datetime.utcnow(),
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)

    # 2️⃣  Send email notification (non-blocking)
    background_tasks.add_task(email_service.notify_owner, payload)

    return schemas.ContactResponse(
        success = True,
        id      = db_msg.id,
        detail  = "Message received. Ahmed will get back to you soon."
    )


@app.get(
    "/api/messages",
    response_model=list[schemas.MessageOut],
    tags=["Admin"]
)
@app.get(
    "/messages",
    response_model=list[schemas.MessageOut],
    include_in_schema=False
)
@limiter.limit("30/minute")  # ✅ محدود للإدارة أيضاً
def list_messages(
    request: Request,  # ← مطلوب للـ rate limiter
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin_key)  # ✅ يتطلب مفتاح إدارة
):
    """
    Return all stored messages (newest first).
    
    ✅ محمي بـ:
    - مفتاح API للإدارة (إلزامي)
    - rate limiting
    """
    return (
        db.query(models.Message)
          .order_by(models.Message.sent_at.desc())
          .offset(skip)
          .limit(limit)
          .all()
    )


@app.delete(
    "/api/messages/{message_id}",
    tags=["Admin"]
)
@app.delete(
    "/messages/{message_id}",
    include_in_schema=False
)
@limiter.limit("30/minute")  # ✅ محدود للحذف
def delete_message(
    request: Request,  # ← مطلوب للـ rate limiter
    message_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin_key)  # ✅ يتطلب مفتاح إدارة
):
    """
    Delete a single message by ID.
    
    ✅ محمي بـ:
    - مفتاح API للإدارة (إلزامي)
    - rate limiting
    """
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(msg)
    db.commit()
    return {"success": True, "deleted_id": message_id}


# Serve the portfolio frontend from the same app
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
