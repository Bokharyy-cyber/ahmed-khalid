# 🔒 دليل تطبيق إصلاحات الأمان - خطوة بخطوة

## ⏱️ الوقت المتوقع: 2-3 ساعات

---

## المرحلة 1️⃣: الإعداد الأولي (30 دقيقة)

### الخطوة 1: تثبيت المكتبات الأمان الجديدة

```bash
cd backend
pip install slowapi email-validator markupsafe
```

**التحقق:**
```bash
pip list | grep -E "slowapi|email-validator|markupsafe"
```

### الخطوة 2: إنشاء .env آمن

```bash
# انسخ الملف الجديد
cp env.example_SECURE .env

# حرّر الملف وأضف:
# 1. مفتاح admin قوي (استخدم أداة توليد)
# 2. بريدك الحقيقي
# 3. تفاصيل Gmail الصحيحة
# 4. نطاقات CORS الخاصة بك
```

**إنشاء مفتاح admin قوي:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
# النتيجة: nRqDxR_p-8Lfh3K9x2m5...
```

**تحديث .env:**
```env
ADMIN_API_KEY=nRqDxR_p-8Lfh3K9x2m5...
OWNER_EMAIL=your_real_email@example.com
GMAIL_USER=your_gmail@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
ALLOWED_ORIGINS=https://bokhary.com,https://www.bokhary.com
ENVIRONMENT=production
```

### الخطوة 3: التأكد من .env في .gitignore

```bash
# تحقق من وجود .env في .gitignore
grep ".env" ../.gitignore

# إذا لم يكن موجوداً، أضفه:
echo ".env" >> ../.gitignore
```

---

## المرحلة 2️⃣: تحديث الكود (1.5 ساعات)

### الخطوة 4: استبدال email_service.py

```bash
# احفظ النسخة القديمة للمرجعية
cp email_service.py email_service.py.backup

# استبدل بالنسخة الآمنة
# انسخ محتوى main_SECURE.py إلى email_service.py
```

**التحقق من الكود الجديد:**
```python
# اختبر الدوال الجديدة:
from email_service import is_safe_email_for_header, sanitize_for_html

# يجب أن تمر:
assert is_safe_email_for_header("user@example.com") == True
assert is_safe_email_for_header("user\n@example.com") == False

# يجب أن تنظف:
result = sanitize_for_html("<script>alert('xss')</script>")
assert "<script>" not in result
print("✅ Email service security checks passed!")
```

### الخطوة 5: استبدال main.py

```bash
# احفظ النسخة القديمة
cp main.py main.py.backup

# استبدل بالنسخة الآمنة
# انسخ محتوى main_SECURE.py إلى main.py
```

**التحقق:**
```bash
# تحقق من الأخطاء النحوية
python -m py_compile main.py
echo "✅ Syntax check passed"

# اختبر الاستيراد
python -c "from main import app; print('✅ Import successful')"
```

### الخطوة 6: تحديث requirements.txt

```bash
# انسخ النسخة الآمنة الجديدة
cp requirements_SECURE.txt requirements.txt

# أعد تثبيت المكتبات
pip install -r requirements.txt
```

---

## المرحلة 3️⃣: الاختبار (30 دقيقة)

### الخطوة 7: اختبر عدم الحماية

```bash
# ابدأ الخادم محلياً
python -m uvicorn main:app --reload

# في terminal آخر، اختبر الـ rate limiting:
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/contact \
    -H "Content-Type: application/json" \
    -d '{"name":"Test","email":"test@example.com","subject":"Test","message":"Test message here"}'
done
# يجب أن يفشل بعد 5 طلبات (429 Too Many Requests) ✅
```

### الخطوة 8: اختبر حماية الإدارة

```bash
# محاولة بدون مفتاح (يجب أن تفشل):
curl http://localhost:8000/api/messages
# النتيجة: 403 Forbidden ✅

# محاولة مع مفتاح خاطئ (يجب أن تفشل):
curl -H "X-Admin-Key: wrong_key" http://localhost:8000/api/messages
# النتيجة: 401 Unauthorized ✅

# محاولة مع مفتاح صحيح (يجب أن تنجح):
curl -H "X-Admin-Key: YOUR_ACTUAL_KEY" http://localhost:8000/api/messages
# النتيجة: 200 OK + رسائل ✅
```

### الخطوة 9: اختبر تنظيف HTML

```python
# انسخ هذا الكود في ملف test_security.py:

from backend.email_service import sanitize_for_html

# اختبارات XSS
xss_attacks = [
    '<script>alert("xss")</script>',
    '<img src=x onerror="alert(\'xss\')">',
    '<iframe src="evil.com"></iframe>',
    '"><script>alert(String.fromCharCode(88,83,83))</script>',
]

for attack in xss_attacks:
    result = sanitize_for_html(attack)
    assert "<script>" not in result, f"Failed to sanitize: {attack}"
    assert "onerror=" not in result, f"Failed to sanitize: {attack}"
    assert "iframe" not in result, f"Failed to sanitize: {attack}"
    print(f"✅ Sanitized: {attack}")

print("\n✅✅✅ All XSS tests passed!")
```

**اشغل الاختبارات:**
```bash
cd ..
python test_security.py
```

### الخطوة 10: اختبر رؤوس الأمان

```bash
# تحقق من رؤوس الأمان:
curl -i http://localhost:8000/api/health | grep -E "X-Content-Type|X-Frame-Options|Content-Security-Policy"

# يجب أن ترى:
# X-Content-Type-Options: nosniff ✅
# X-Frame-Options: DENY ✅
# Content-Security-Policy: default-src 'self'... ✅
```

---

## المرحلة 4️⃣: النشر (30 دقيقة)

### الخطوة 11: تحديث متغيرات البيئة في الخادم

**على Render أو أي منصة أخرى:**

1. اذهب إلى لوحة تحكم التطبيق
2. ابحث عن "Environment" أو "Config Vars"
3. أضف/حدث المتغيرات:

```
ADMIN_API_KEY = [مفتاح قوي جديد]
OWNER_EMAIL = [بريدك الحقيقي]
GMAIL_USER = [بريدك الحقيقي]
GMAIL_APP_PASSWORD = [كلمة مرور التطبيق]
ALLOWED_ORIGINS = https://bokhary.com,https://www.bokhary.com
ENVIRONMENT = production
DATABASE_URL = [عنوان قاعدة البيانات]
```

### الخطوة 12: نشر التحديثات

```bash
# التأكد من أن .env في .gitignore:
git status
# لا يجب أن ترى .env

# أضف الملفات الجديدة:
git add backend/main.py backend/email_service.py backend/requirements.txt
git add .gitignore

# التزم بالتغييرات:
git commit -m "🔒 Fix critical security vulnerabilities"

# ادفع إلى Render/المنصة:
git push origin main

# تحقق من لوحة التحكم للتأكد من نجاح النشر
```

### الخطوة 13: التحقق بعد النشر

```bash
# اختبر الخادم الجديد:
curl https://bokhary.com/api/health

# اختبر الرسائل (يجب أن تفشل بدون مفتاح):
curl https://bokhary.com/api/messages
# النتيجة: 403 ✅

# اختبر contact form:
curl -X POST https://bokhary.com/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test Message",
    "message": "This is a test message from the security update."
  }'
# يجب أن ترى: {"success": true, ...} ✅
```

---

## 📋 قائمة التحقق النهائية

- [ ] تثبيت المكتبات الجديدة (slowapi, email-validator)
- [ ] إنشاء .env آمن مع مفاتيح قوية
- [ ] التأكد من .env في .gitignore
- [ ] استبدال email_service.py بالنسخة الآمنة
- [ ] استبدال main.py بالنسخة الآمنة
- [ ] تحديث requirements.txt
- [ ] اختبار rate limiting محلياً
- [ ] اختبار حماية الإدارة
- [ ] اختبار تنظيف HTML/XSS
- [ ] اختبار رؤوس الأمان
- [ ] تحديث متغيرات البيئة في الخادم
- [ ] النشر إلى الإنتاج
- [ ] التحقق من الخادم الجديد

---

## 🎓 نصائح إضافية

### تدوير مفتاح Admin بانتظام

```bash
# كل 90 يوم، توليد مفتاح جديد:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# حدث في .env والخادم، ثم احذف المفتاح القديم
```

### مراقبة الأخطاء الأمنية

أضف logging في main.py:

```python
import logging

logger = logging.getLogger("security")

# في require_admin_key:
logger.warning(f"Failed admin auth attempt from {request.client.host}")

# في email_service:
logger.warning(f"Suspicious email format: {payload.email}")
```

### استخدام WAF

أوصي باستخدام CloudFlare:
1. اذهب إلى cloudflare.com
2. أضف نطاقك
3. فعّل "Web Application Firewall"
4. فعّل "Bot Management"

---

## 📞 الدعم والمساعدة

إذا واجهت مشاكل:

1. **تحقق من السجلات:**
   ```bash
   tail -f logs/app.log
   ```

2. **اختبر الاتصال:**
   ```bash
   python -c "import email_service; print('✅ Import OK')"
   ```

3. **التحقق من البيئة:**
   ```bash
   python -c "import os; print('ADMIN_API_KEY set:', bool(os.getenv('ADMIN_API_KEY')))"
   ```

---

**استمتع بموقع آمن أكثر! 🛡️**
