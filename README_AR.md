# 🛡️ BOKHARY - المشروع بعد الإصلاح الأمني

## ✅ تم إصلاح جميع الثغرات الأمنية!

---

## 🚀 خطوات التشغيل السريعة:

### 1️⃣ **إعداد ملف .env**

```bash
cd backend
cp env.example .env
```

**ثم افتح `.env` وعدّل:**

```env
# ✅ 1. توليد مفتاح admin قوي جديد
# اشغل هذا في terminal:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
ADMIN_API_KEY=ضع_المفتاح_هنا

# ✅ 2. ضع بريدك الحقيقي هنا (سيستقبل الرسائل)
OWNER_EMAIL=your_real_email@gmail.com

# ✅ 3. ضع بيانات Gmail (استخدم App Password، ليس كلمة السر الأصلية)
# اذهب إلى: https://myaccount.google.com/apppasswords
GMAIL_USER=your_gmail@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

# ✅ 4. ضع نطاق موقعك
# مثال: https://bokhary.com,https://www.bokhary.com
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# ✅ 5. اترك بقية الإعدادات كما هي
```

---

### 2️⃣ **تثبيت المكتبات**

```bash
pip install -r requirements.txt
```

---

### 3️⃣ **تشغيل الخادم محلياً**

```bash
python -m uvicorn main:app --reload
```

ثم افتح: `http://localhost:8000`

---

### 4️⃣ **نشر على Render أو أي منصة أخرى**

**متغيرات البيئة المطلوبة:**
```
ADMIN_API_KEY = [مفتاح قوي]
OWNER_EMAIL = [بريدك الحقيقي]
GMAIL_USER = [بريدك على Gmail]
GMAIL_APP_PASSWORD = [كلمة مرور التطبيق]
ALLOWED_ORIGINS = https://bokhary.com
ENVIRONMENT = production
DATABASE_URL = [رابط قاعدة البيانات]
```

---

## 🔒 ما تم إصلاحه:

| الثغرة | الحل |
|------|------|
| ❌ HTML Injection | ✅ تنظيف جميع المدخلات بـ `escape()` |
| ❌ لا حماية للمسارات | ✅ مفتاح API إلزامي للإدارة |
| ❌ Email Header Injection | ✅ التحقق من سلامة البريد |
| ❌ Spam بلا حدود | ✅ Rate limiting (5 رسائل/دقيقة) |
| ❌ CORS مفتوح | ✅ حماية محددة الضروري فقط |
| ❌ لا CSP headers | ✅ Content Security Policy محكم |
| ❌ بيانات حساسة معروضة | ✅ إخفاء تام وإجبارية |

---

## 🧪 اختبارات سريعة:

### اختبر Rate Limiting:
```bash
# الطلب الأول - نجاح:
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{"name":"Ahmed","email":"test@example.com","subject":"Test","message":"Hello this is a test message"}'

# بعد 5 طلبات متتالية - فشل:
# ستحصل على: 429 Too Many Requests ✅
```

### اختبر حماية الإدارة:
```bash
# بدون مفتاح - يفشل:
curl http://localhost:8000/api/messages
# النتيجة: 403 Forbidden ✅

# مع مفتاح خاطئ - يفشل:
curl -H "X-Admin-Key: wrong" http://localhost:8000/api/messages
# النتيجة: 401 Unauthorized ✅

# مع مفتاح صحيح - ينجح:
curl -H "X-Admin-Key: YOUR_ACTUAL_KEY" http://localhost:8000/api/messages
# النتيجة: 200 OK ✅
```

---

## 📁 هيكل المشروع:

```
BOKHARY_FIXED/
├── backend/
│   ├── main.py                 ✅ تم إصلاحه
│   ├── email_service.py        ✅ تم إصلاحه
│   ├── requirements.txt         ✅ محدث
│   ├── env.example             ✅ محدث
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── render.yaml
├── images/                      (صور الموقع)
├── index.html
├── script.js
└── styles.css
```

---

## ⚠️ نقاط مهمة:

1. **لا تشارك .env** - أضفه في `.gitignore`
2. **استخدم مفتاح قوي** - الأمان يعتمد عليه
3. **استخدم HTTPS فقط** - في الإنتاج
4. **حدث كل 3 أشهر** - غيّر مفتاح admin بانتظام
5. **فعّل logging** - راقب محاولات الوصول المريبة

---

## 🆘 مشاكل شائعة:

### المشكلة: `ModuleNotFoundError: No module named 'slowapi'`
**الحل:**
```bash
pip install slowapi
```

### المشكلة: البريد لا يُرسل
**الحل:**
1. تأكد من تفعيل GMAIL_USER و GMAIL_APP_PASSWORD
2. استخدم App Password من Google، ليس كلمة السر الأصلية
3. افتح `email_service.py` وتحقق من الأخطاء

### المشكلة: لا يمكن الوصول إلى `/api/messages`
**الحل:**
```bash
# تأكد من وضع المفتاح:
curl -H "X-Admin-Key: your_key_from_env" http://localhost:8000/api/messages
```

---

## 📞 المساعدة:

اقرأ `BOKHARY_SECURITY_AUDIT.md` لفهم كل ثغرة
اقرأ `IMPLEMENTATION_GUIDE.md` للتفاصيل الكاملة

---

**موقعك الآن آمن! 🛡️✅**
