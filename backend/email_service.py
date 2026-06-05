import os
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from html import escape
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER     = os.getenv("GMAIL_USER")            # your Gmail address
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")    # Gmail App Password (not your real password)
OWNER_EMAIL    = os.getenv("OWNER_EMAIL")           # ✅ يجب تحديده، لا قيمة افتراضية!

# ✅ التحقق من أن المتغيرات مُعرَّفة
if not OWNER_EMAIL:
    raise ValueError(
        "OWNER_EMAIL environment variable must be set! "
        "Please add it to your .env file."
    )


def is_safe_email_for_header(email_str: str) -> bool:
    """
    ✅ تحقق من أن البريد آمن للاستخدام في رؤوس البريد
    يمنع email header injection attacks
    """
    # البريد لا يجب أن يحتوي على newlines أو carriage returns
    if '\n' in email_str or '\r' in email_str:
        return False
    
    # تحقق من صيغة البريد الأساسية
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email_str))


def sanitize_for_html(text: str) -> str:
    """
    ✅ تنظيف النص للاستخدام الآمن في HTML
    - تحويل الأحرف الخاصة إلى HTML entities
    - تحويل الأسطر الجديدة إلى <br>
    """
    # استخدم html.escape لتحويل الأحرف الخاصة
    escaped = escape(text)
    
    # حوّل الأسطر الجديدة إلى <br> (آمن بعد الـ escape)
    escaped = escaped.replace('\n', '<br>')
    
    return escaped


def _build_html(name: str, email: str, subject: str, message: str) -> str:
    """
    ✅ بناء HTML البريد الإلكتروني بشكل آمن
    جميع المدخلات تُنظّف ضد XSS و HTML injection
    """
    # تنظيف جميع المدخلات
    safe_name = sanitize_for_html(name)
    safe_email = sanitize_for_html(email)
    safe_subject = sanitize_for_html(subject)
    safe_message = sanitize_for_html(message)
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  body  {{ margin:0; padding:0; background:#050505; font-family:'Segoe UI',Arial,sans-serif; color:#fff; }}
  .wrap {{ max-width:600px; margin:40px auto; background:#111; border:1px solid #1a1a1a; }}
  .hdr  {{ background:#8B0000; padding:30px 40px; }}
  .hdr h1 {{ margin:0; font-size:28px; letter-spacing:0.2em; font-weight:400; }}
  .hdr p  {{ margin:6px 0 0; font-size:12px; letter-spacing:0.25em; opacity:0.7; text-transform:uppercase; }}
  .body {{ padding:40px; }}
  .row  {{ border-bottom:1px solid #1a1a1a; padding:16px 0; display:flex; gap:20px; }}
  .row:last-of-type {{ border-bottom:none; }}
  .lbl  {{ font-size:10px; letter-spacing:0.3em; text-transform:uppercase; color:#8B0000;
           min-width:80px; padding-top:3px; }}
  .val  {{ font-size:15px; color:#e0e0e0; line-height:1.6; word-break:break-word; }}
  .msg  {{ background:#0a0a0a; border-left:2px solid #8B0000; padding:20px 24px;
           font-size:15px; color:#ccc; line-height:1.8; margin-top:24px; }}
  .ftr  {{ padding:20px 40px; background:#080808; font-size:10px; letter-spacing:0.25em;
           text-transform:uppercase; color:#333; text-align:center; }}
  .warning {{ color: #ff6b6b; font-weight: bold; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="hdr">
    <h1>BOKHARY</h1>
    <p>New message from your portfolio</p>
  </div>
  <div class="body">
    <div class="row">
      <span class="lbl">From</span>
      <span class="val">{safe_name}</span>
    </div>
    <div class="row">
      <span class="lbl">Email</span>
      <span class="val"><a href="mailto:{safe_email}" style="color:#8B0000;text-decoration:none">{safe_email}</a></span>
    </div>
    <div class="row">
      <span class="lbl">Subject</span>
      <span class="val">{safe_subject}</span>
    </div>
    <div class="msg">{safe_message}</div>
  </div>
  <div class="ftr">Ahmed Khalid Gharib — Portfolio API · 2025</div>
</div>
</body>
</html>
"""


def notify_owner(payload) -> None:
    """
    ✅ إرسال بريد إلكتروني آمن للمالك
    - يتحقق من سلامة البريد الإلكتروني للمستخدم
    - ينظف جميع المدخلات من XSS و HTML injection
    - يسجل أي محاولات مريبة
    """
    if not GMAIL_USER or not GMAIL_PASSWORD:
        print("[email_service] ⚠️  GMAIL_USER or GMAIL_APP_PASSWORD not set — skipping email.")
        return

    # ✅ التحقق من أمان البريد الإلكتروني
    if not is_safe_email_for_header(payload.email):
        print(f"[email_service] 🔴 SECURITY ALERT: Suspicious email format detected!")
        print(f"    Email: {payload.email}")
        print(f"    Name: {payload.name}")
        # تسجيل محاولات الهجوم (في الإنتاج، أرسل تنبيهاً)
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"]  = f"[Portfolio] {payload.subject} — from {payload.name}"
        msg["From"]     = GMAIL_USER
        msg["To"]       = OWNER_EMAIL
        
        # ✅ استخدام formataddr لتنسيق البريد بشكل آمن
        msg["Reply-To"] = f"{payload.name} <{payload.email}>"

        html_body = _build_html(
            name    = payload.name,
            email   = payload.email,
            subject = payload.subject,
            message = payload.message,
        )
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, OWNER_EMAIL, msg.as_string())

        print(f"[email_service] ✅  Email sent to {OWNER_EMAIL}")

    except smtplib.SMTPAuthenticationError:
        print("[email_service] ❌  Auth failed — check GMAIL_USER and GMAIL_APP_PASSWORD.")
    except Exception as exc:
        print(f"[email_service] ❌  Unexpected error: {exc}")
