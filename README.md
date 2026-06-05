# BOKHARY Portfolio - Secured Version 🛡️

This is the **security-hardened version** of your BOKHARY portfolio website. All critical vulnerabilities have been fixed.

## ✅ What Was Fixed

| Issue | Fix |
|-------|-----|
| HTML Injection in Emails | ✅ All inputs escaped using `html.escape()` |
| Unprotected Admin Endpoints | ✅ Mandatory API key authentication |
| Email Header Injection | ✅ Email validation and sanitization |
| No Rate Limiting | ✅ Rate limiting enabled (5 messages/minute) |
| Overly Permissive CORS | ✅ Restricted to necessary methods/headers |
| Missing Security Headers | ✅ Added CSP, X-Frame-Options, etc. |
| Hardcoded Credentials | ✅ All removed, using environment variables |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Setup (Choose one)

**On Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```bash
setup.bat
```

**Manual setup:**
```bash
cd backend
pip install -r requirements.txt
cp env.example .env
```

### Step 2: Configure Environment

Edit `backend/.env` with your actual values:

```env
# Generate a strong key:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
ADMIN_API_KEY=your_strong_key_here

# Your email (receives messages)
OWNER_EMAIL=your_email@example.com

# Gmail configuration
GMAIL_USER=your_gmail@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

# Your domain
ALLOWED_ORIGINS=https://bokhary.com,https://www.bokhary.com
```

### Step 3: Run

```bash
cd backend
python -m uvicorn main:app --reload
```

Open: http://localhost:8000

---

## 📊 Security Features

### Rate Limiting
- **Contact form:** 5 messages per minute per IP
- **Admin endpoints:** 30 requests per minute per IP

### Authentication
- All admin endpoints require `X-Admin-Key` header
- Secure comparison using `secrets.compare_digest()`

### Input Validation
- Email format validation
- Message content sanitization
- XSS prevention with HTML escaping

### HTTP Security Headers
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Content-Security-Policy` (strict)
- `Strict-Transport-Security` (in production)

---

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI application (secured)
├── email_service.py     # Email handler (secured)
├── database.py          # Database configuration
├── models.py            # ORM models
├── schemas.py           # Pydantic schemas
├── requirements.txt     # Dependencies
└── env.example          # Example environment file

images/                  # Website images
index.html               # Frontend
script.js                # Client-side JavaScript
styles.css               # Styling
```

---

## 🔑 API Endpoints

### Public Endpoints

**POST /api/contact**
- Send a contact message
- Rate limited: 5/minute per IP
- Request body:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Collaboration",
    "message": "Your message here (min 10 chars)"
  }
  ```

**GET /api/health**
- Health check endpoint

### Admin Endpoints (Require API Key)

**GET /api/messages**
- List all messages
- Header: `X-Admin-Key: your_api_key`

**DELETE /api/messages/{message_id}**
- Delete a specific message
- Header: `X-Admin-Key: your_api_key`

---

## 🧪 Testing

### Test Rate Limiting
```bash
# Should succeed:
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","subject":"Test","message":"Test message here"}'

# After 5 attempts: 429 Too Many Requests ✅
```

### Test Admin Protection
```bash
# Without key (should fail):
curl http://localhost:8000/api/messages
# Response: 403 Forbidden ✅

# With wrong key (should fail):
curl -H "X-Admin-Key: wrong_key" http://localhost:8000/api/messages
# Response: 401 Unauthorized ✅

# With correct key (should succeed):
curl -H "X-Admin-Key: YOUR_KEY_FROM_ENV" http://localhost:8000/api/messages
# Response: 200 OK ✅
```

---

## 🌍 Deploying to Production

### Environment Variables Needed

```env
ADMIN_API_KEY=your_strong_key
OWNER_EMAIL=your_email@example.com
GMAIL_USER=your_gmail@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
ALLOWED_ORIGINS=https://bokhary.com,https://www.bokhary.com
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host/db
```

### Recommended Deployment Platforms
- Render.com (free tier available)
- Railway.app
- Heroku
- AWS/Google Cloud/Azure

### Post-Deployment Checklist
- [ ] HTTPS enabled
- [ ] Environment variables set
- [ ] Database migrated
- [ ] Email service tested
- [ ] Admin key changed from example
- [ ] ALLOWED_ORIGINS updated
- [ ] Rate limiting working
- [ ] Security headers present

---

## 🔐 Security Best Practices

1. **Rotate Admin Key** - Every 90 days
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Use HTTPS** - Never use HTTP in production

3. **Monitor Logs** - Check for suspicious activity

4. **Keep Dependencies Updated**
   ```bash
   pip list --outdated
   pip install --upgrade [package_name]
   ```

5. **Enable WAF** - Use CloudFlare or similar

6. **Backup Database** - Regular automated backups

---

## 🚨 Common Issues

### Issue: `ModuleNotFoundError: No module named 'slowapi'`
**Solution:** `pip install slowapi`

### Issue: Email not sending
**Solutions:**
1. Check GMAIL_USER and GMAIL_APP_PASSWORD are correct
2. Use App Password, not your actual Gmail password
3. Enable "Less secure app access" if needed
4. Check OWNER_EMAIL is a valid email

### Issue: 401 Unauthorized on admin endpoints
**Solution:** Make sure to include the `X-Admin-Key` header:
```bash
curl -H "X-Admin-Key: your_actual_key_from_env" http://localhost:8000/api/messages
```

---

## 📖 Documentation

- `README_AR.md` - Arabic quick start guide
- `BOKHARY_SECURITY_AUDIT.md` - Complete security audit (Arabic)
- `IMPLEMENTATION_GUIDE.md` - Detailed implementation steps (Arabic)

---

## 📝 License

This project is part of BOKHARY Portfolio.

---

## 🆘 Support

For security issues, contact immediately.
For other issues, check the documentation files.

---

**Your website is now secure! 🛡️✅**
