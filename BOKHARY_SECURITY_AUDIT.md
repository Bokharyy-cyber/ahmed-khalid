# 🔒 تقرير أمان موقع BOKHARY - أغسطس 2026

## ⚠️ ملخص تنفيذي
تم اكتشاف **4 ثغرات حرجة** و **3 ثغرات متوسطة** في الموقع تتطلب إصلاح فوري.

---

## 🔴 الثغرات الحرجة (CRITICAL)

### 1. **HTML Injection في خدمة البريد الإلكتروني** ⚠️ [CRITICAL]

**الملف:** `backend/email_service.py` (السطور 14-64)

**المشكلة:**
يتم إدراج بيانات المستخدم مباشرة في HTML دون تنظيف:

```python
# ❌ UNSAFE CODE
def _build_html(name: str, email: str, subject: str, message: str) -> str:
    return f"""
    ...
    <span class="val">{name}</span>  <!-- ✗ HTML Injection! -->
    ...
    <span class="val"><a href="mailto:{email}">...</a></span>  <!-- ✗ XSS -->
    ...
    <span class="val">{subject}</span>  <!-- ✗ HTML Injection -->
    ...
    <div class="msg">{message}</div>  <!-- ✗ Can inject scripts -->
    """
```

**السيناريو الخطر:**
```json
{
  "name": "<img src=x onerror='alert(\"XSS\")'>",
  "email": "hacker@evil.com\nbcc: attacker@evil.com",
  "subject": "</span></div><script>alert('Hacked')</script>",
  "message": "<iframe src='https://phishing.com'></iframe>"
}
```

**الحل:**
استخدم HTML escaping:

```python
# ✅ SECURE CODE
from html import escape

def _build_html(name: str, email: str, subject: str, message: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    ...
    <span class="val">{escape(name)}</span>
    <span class="val"><a href="mailto:{escape(email)}">{escape(email)}</a></span>
    <span class="val">{escape(subject)}</span>
    <div class="msg">{escape(message)}</div>
    ...
    """
```

---

### 2. **عدم وجود حماية API للرسائل الحساسة** ⚠️ [CRITICAL]

**الملف:** `backend/main.py` (السطور 117-143)

**المشكلة:**
إذا لم تعيّن متغير البيئة `ADMIN_API_KEY`، يمكن لأي شخص الوصول لجميع الرسائل:

```python
# ❌ UNSAFE CODE
def require_admin_key(x_admin_key: str | None = Header(default=None)):
    if not ADMIN_API_KEY:  # ← إذا كان فارغاً، لا يوجد حماية!
        return
    if not x_admin_key or not secrets.compare_digest(x_admin_key, ADMIN_API_KEY):
        raise HTTPException(status_code=401, detail="Invalid or missing admin key")
```

**الهجوم:**
```bash
curl https://bokhary.com/api/messages
# ✗ يعيد جميع الرسائل بدون حماية!
```

**الحل:**

```python
# ✅ SECURE CODE
def require_admin_key(x_admin_key: str | None = Header(default=None)):
    if not ADMIN_API_KEY:
        # ✗ فشل آمن - لا يوجد مفتاح مُعرّف
        raise HTTPException(
            status_code=403, 
            detail="Admin panel is not configured"
        )
    if not x_admin_key or not secrets.compare_digest(x_admin_key, ADMIN_API_KEY):
        raise HTTPException(status_code=401, detail="Invalid or missing admin key")
```

---

### 3. **Email Header Injection** ⚠️ [CRITICAL]

**الملف:** `backend/email_service.py` (السطر 81)

**المشكلة:**
البريد الإلكتروني للمستخدم يُدرج مباشرة في رأس البريد دون التحقق من الأحرف الخاصة:

```python
# ❌ UNSAFE CODE
msg["Reply-To"] = payload.email  # يمكن احتواء newlines!
```

**السيناريو الخطر:**
```
البريد: victim@example.com\nbcc:attacker@evil.com
# النتيجة: البريد يُرسل أيضاً إلى attacker@evil.com!
```

**الحل:**

```python
# ✅ SECURE CODE
import email.utils

# التحقق من عدم وجود أحرف إدراج الرؤوس
def is_safe_email_for_header(email_str: str) -> bool:
    """تحقق من عدم احتواء البريد على أحرف خطرة"""
    return '\n' not in email_str and '\r' not in email_str

if is_safe_email_for_header(payload.email):
    msg["Reply-To"] = email.utils.formataddr(("", payload.email))
else:
    # تسجيل الرسالة المريبة
    print(f"[SECURITY] Suspicious email format detected: {payload.email}")
```

---

### 4. **عدم وجود Rate Limiting على Contact Endpoint** ⚠️ [CRITICAL]

**المشكلة:**
يمكن لأي شخص إرسال آلاف الرسائل لإغراق قاعدة البيانات والبريد:

```python
# ❌ لا يوجد حماية ضد spam!
@app.post("/api/contact")
async def submit_contact(payload: schemas.ContactCreate, ...):
    # أي شخص يمكنه الإرسال بلا حدود
```

**الحل:**
استخدم `SlowAPI` أو `FastAPI-Limiter`:

```python
# ✅ SECURE CODE
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/contact")
@limiter.limit("5/minute")  # 5 رسائل كل دقيقة لكل IP
async def submit_contact(request: Request, payload: schemas.ContactCreate, ...):
    ...
```

---

## 🟡 الثغرات المتوسطة (MEDIUM)

### 5. **CORS مفتوحة جداً**

**الملف:** `backend/main.py` (السطور 32-38)

**المشكلة:**
```python
# ❌ TOO PERMISSIVE
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # ← كل الطرق!
    allow_headers=["*"],  # ← كل الرؤوس!
)
```

**الحل:**
```python
# ✅ SECURE
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],  # ← فقط اللازم
    allow_headers=["Content-Type"],  # ← الرؤوس الضرورية فقط
)
```

---

### 6. **بيانات حساسة في الكود الافتراضي**

**الملف:** `backend/email_service.py` (السطر 11)

```python
# ❌ بيان البريد الحقيقي في الكود!
OWNER_EMAIL = os.getenv("OWNER_EMAIL", "ahmed8khale162d6@gmail.com")
```

**الحل:**
```python
# ✅ SECURE
OWNER_EMAIL = os.getenv("OWNER_EMAIL")
if not OWNER_EMAIL:
    raise ValueError("OWNER_EMAIL environment variable must be set!")
```

---

### 7. **عدم وجود Content Security Policy (CSP)**

**المشكلة:**
لا يوجد رأس CSP لحماية من XSS والهجمات الأخرى.

**الحل:**
```python
# ✅ أضف في main.py
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

class CSPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' https:; "
            "font-src 'self'; "
            "connect-src 'self' https://api.example.com"
        )
        return response

app.add_middleware(CSPMiddleware)
```

---

## 📋 خطة الإصلاح الأولويات

| الأولوية | الثغرة | الوقت المتوقع | الحالة |
|---------|--------|--------------|--------|
| 🔴 P0 | HTML Injection | 30 دقيقة | حرج جداً |
| 🔴 P0 | عدم حماية المسارات | 20 دقيقة | حرج جداً |
| 🔴 P0 | Email Header Injection | 20 دقيقة | حرج جداً |
| 🔴 P0 | Rate Limiting | 45 دقيقة | حرج جداً |
| 🟡 P1 | CORS | 15 دقيقة | متوسط |
| 🟡 P1 | CSP Headers | 20 دقيقة | متوسط |
| 🟡 P1 | الأسرار الحساسة | 10 دقائق | متوسط |

---

## 🛠️ خطوات التنفيذ الفورية

### الخطوة 1: تثبيت المكتبات
```bash
pip install slowapi email-validator markupsafe
```

### الخطوة 2: إنشء ملف `.env` آمن
```env
ADMIN_API_KEY=your_super_secret_key_here_CHANGE_ME
OWNER_EMAIL=your_real_email@gmail.com
GMAIL_USER=your_gmail@gmail.com
GMAIL_APP_PASSWORD=your_app_password_here
ALLOWED_ORIGINS=https://bokhary.com,https://www.bokhary.com
DATABASE_URL=postgresql://...
```

### الخطوة 3: تحديث `backend/email_service.py`
```python
from html import escape
import re

# دالة للتحقق من البريد
def is_valid_email_for_header(email_str: str) -> bool:
    return '\n' not in email_str and '\r' not in email_str

def _build_html(name: str, email: str, subject: str, message: str) -> str:
    # تنظيف جميع المدخلات
    safe_name = escape(name)
    safe_email = escape(email)
    safe_subject = escape(subject)
    safe_message = escape(message)
    
    # تحويل الأسطر الجديدة إلى <br>
    safe_message = safe_message.replace('\n', '<br>')
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    ...
    <span class="val">{safe_name}</span>
    <span class="val"><a href="mailto:{safe_email}">{safe_email}</a></span>
    <span class="val">{safe_subject}</span>
    <div class="msg">{safe_message}</div>
    ...
    """
```

---

## 🔐 التوصيات الإضافية

1. **استخدم HTTPS فقط** - أضف HSTS header
2. **فعّل تسجيل الأحداث** - سجّل جميع محاولات الوصول
3. **استخدم Web Application Firewall (WAF)** - مثل CloudFlare
4. **قم بفحص أمان دوري** - استخدم OWASP ZAP أو Burp Suite
5. **حدث البكتات** - ابقَ محدثاً مع أحدث الإصدارات
6. **استخدم SQL parameterized queries** - (بالفعل تستخدم ORM ✓)
7. **فعّل logging وmonitoring** - استخدم Sentry أو مشابه

---

## 📞 الدعم
إذا كنت بحاجة لمساعدة في تطبيق هذه الإصلاحات، تواصل معي!

---

**التاريخ:** 2026-06-05  
**تقييم الأمان:** ⭐⭐ (2/5) - يحتاج إصلاح فوري!  
**الحالة:** 🔴 ليس آمناً للعام
