# BOKHARY Portfolio — Backend API

FastAPI backend for Ahmed Khalid Gharib's personal portfolio.

---

## Stack

| Layer      | Technology          |
|------------|---------------------|
| Framework  | FastAPI             |
| Database   | SQLite (local) / PostgreSQL (Render) |
| ORM        | SQLAlchemy          |
| Email      | Gmail SMTP (smtplib) |
| Hosting    | Render (free tier)  |

---

## Project Structure

```
bokhary-backend/
├── main.py           # FastAPI app + routes
├── database.py       # DB engine & session
├── models.py         # SQLAlchemy ORM models
├── schemas.py        # Pydantic request/response
├── email_service.py  # Gmail notification
├── requirements.txt
├── render.yaml       # Render deployment config
└── .env.example      # Environment variables template
```

---

## API Endpoints

| Method | Endpoint            | Description                      |
|--------|---------------------|----------------------------------|
| GET    | `/api/health`       | Health check                     |
| POST   | `/api/contact`      | Submit contact form              |
| GET    | `/api/messages`     | List all messages (admin)        |
| DELETE | `/api/messages/{id}` | Delete a message (admin)         |

### POST `/api/contact` — Request Body

```json
{
  "name":    "John Doe",
  "email":   "john@example.com",
  "subject": "Collaboration",
  "message": "Hi Ahmed, I'd like to..."
}
```

### POST `/api/contact` — Response

```json
{
  "success": true,
  "id": 1,
  "detail": "Message received. Ahmed will get back to you soon."
}
```

---

## Local Setup

> Legacy aliases `/contact`, `/messages`, and `/messages/{id}` still work for backward compatibility, but the recommended paths are under `/api`.


### 1. Clone & install

```bash
git clone https://github.com/YOUR_USERNAME/bokhary-backend.git
cd bokhary-backend
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Open .env and fill in your values
```

### 3. Run

```bash
uvicorn main:app --reload
```

API + frontend will be live at: `http://localhost:8000`  
Swagger docs at:         `http://localhost:8000/docs`

---

## Gmail App Password Setup

> Required for email notifications.

1. Go to [https://myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (if not already on)
3. Go to [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
4. Create a new app password → name it **"BOKHARY Portfolio"**
5. Copy the 16-character password into `.env` as `GMAIL_APP_PASSWORD`

---

## Deploy to Render (Free)

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial backend"
git remote add origin https://github.com/YOUR_USERNAME/bokhary-backend.git
git push -u origin main
```

### Step 2 — Create Render account

Go to [https://render.com](https://render.com) → Sign up with GitHub.

### Step 3 — Create PostgreSQL database

1. Dashboard → **New** → **PostgreSQL**
2. Name: `bokhary-db`
3. Plan: **Free**
4. Click **Create Database**
5. Copy the **Internal Database URL**

### Step 4 — Create Web Service

1. Dashboard → **New** → **Web Service**
2. Connect your GitHub repo
3. Settings:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

### Step 5 — Set Environment Variables

In the Render dashboard → your service → **Environment**:

| Key                  | Value                            |
|----------------------|----------------------------------|
| `DATABASE_URL`       | (paste Internal PostgreSQL URL)  |
| `GMAIL_USER`         | your Gmail address               |
| `GMAIL_APP_PASSWORD` | your 16-char App Password        |
| `OWNER_EMAIL`        | ahmed8khale162d6@gmail.com       |

### Step 6 — Deploy

Click **Deploy** — Render will build and start your API.

Your API URL will be:  
```
https://bokhary-portfolio-api.onrender.com
```

---

## Connect Frontend to Backend

The frontend is served by the same FastAPI app, so the contact form uses `/api/contact` automatically.

---

## Notes

- Free Render services **spin down after 15 min of inactivity** — first request may take ~30 sec to wake up.
- The free PostgreSQL database on Render expires after **90 days** — upgrade or re-create it.
- Never commit your real `.env` file to GitHub — only commit `.env.example`.


## Admin protection

Set `ADMIN_API_KEY` in your environment to protect `/api/messages` and `/api/messages/{id}`. Send it in the `X-Admin-Key` header when calling those endpoints.
