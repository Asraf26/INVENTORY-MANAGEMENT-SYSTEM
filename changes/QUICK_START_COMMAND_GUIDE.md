# 🚀 QUICK START GUIDE - 5 Minutes to Running System

## Step-by-Step Execution

### Terminal Commands

```bash
# 1. Navigate to backend folder
cd backend

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Run migrations (first time only)
python manage.py migrate

# 4. Start the server (keep running)
python manage.py runserver
```

## URLs

| Purpose | URL |
|---------|-----|
| **Login** | http://localhost:8000/login.html |
| **Sign Up** | http://localhost:8000/signup.html |
| **Dashboard** | http://localhost:8000/index.html |

## Demo Login

```
Username: admin
Password: admin
```

## File Changes Made

✅ **Created signup component:**
- `frontend/signup.html` - Complete signup page with validation
- `backend/inventory_app/auth_views.py` - Added signup() function
- `backend/inventory_system/urls.py` - Added /api/signup/ endpoint

✅ **Updated login page:**
- `frontend/login.html` - Added link to signup page

## Project Structure

```
backend/
├── inventory_system/
│   ├── settings.py (Django config)
│   └── urls.py (API routes)
│
└── inventory_app/
    ├── auth_views.py (🆕 signup function added)
    ├── models.py (Database tables)
    └── views.py (Business logic)

frontend/
├── login.html (Login page - updated with signup link)
├── signup.html (🆕 New signup page)
├── index.html (Dashboard)
└── assets/
    ├── css/style.css
    └── js/ (API & UI scripts)
```

## Authentication Endpoints

### Login
**POST** `/api/login/`
```json
{
  "username": "admin",
  "password": "admin"
}
```

### Signup
**POST** `/api/signup/`
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123",
  "password_confirm": "password123"
}
```

### Logout
**POST** `/api/logout/`

## Database

- **Type:** SQLite
- **File:** `backend/db.sqlite3`
- **Tables:** User accounts, Products, Warehouses, Inventory, Orders

## Testing

### Test Login
1. Go to http://localhost:8000/login.html
2. Enter: `admin` / `admin`
3. Should redirect to dashboard

### Test Signup
1. Go to http://localhost:8000/signup.html
2. Create new account
3. Login with new credentials

## Common Issues

| Issue | Solution |
|-------|----------|
| "Can't connect to localhost:8000" | Start server: `python manage.py runserver` |
| "ModuleNotFoundError" | Install dependencies: `pip install -r requirements.txt` |
| "Database error" | Run migrations: `python manage.py migrate` |

---

**See [COMPLETE_DOCUMENTATION.md](./COMPLETE_DOCUMENTATION.md) for detailed explanation!**
