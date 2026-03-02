# Complete System Running Guide

## Quick Start

### Step 1: Start the Backend (Django)
```powershell
cd c:\Users\asraf\Desktop\INVENTORY\backend
# Activate virtual environment if not already active
.\.venv\Scripts\Activate.ps1

# Start Django server on port 8000
python manage.py runserver
```
Expected output: `Starting development server at http://127.0.0.1:8000/`

### Step 2: Start the Frontend (HTTP Server)
In a NEW terminal:
```powershell
cd c:\Users\asraf\Desktop\INVENTORY\frontend
# Start Python HTTP server on port 8001
python -m http.server 8001
```
Expected output: `Serving HTTP on 0.0.0.0 port 8001`

### Step 3: Access the Application
1. Open browser to: **http://localhost:8001/login.html**
2. Login with credentials:
   - Username: `admin`
   - Password: `admin123`
3. Dashboard opens at: **http://localhost:8001/index.html**

---

## What's Working

### ✅ Backend (Django on port 8000)
- [x] Database with 10 models
- [x] 40+ REST API endpoints
- [x] Authentication endpoint (`/api/login/`)
- [x] Admin panel (`/admin/`)
- [x] CORS enabled
- [x] Static files configured

### ✅ Frontend (Port 8001)
- [x] Login page with validation
- [x] Dashboard with 9 sections
- [x] CSS styling (relative paths)
- [x] JavaScript modules
- [x] Chart visualizations
- [x] API integration
- [x] Session management
- [x] Logout functionality

---

## Login Flow

```
1. User goes to http://localhost:8001/login.html
2. User enters: admin / admin123
3. Form sends POST to http://localhost:8000/api/login/
4. Django validates credentials
5. Backend returns user object with success=true
6. Frontend stores user in localStorage
7. Frontend redirects to http://localhost:8001/index.html
8. Dashboard loads and displays user data
9. Click logout → clears session → returns to login
```

---

## Testing Checklist

### Test 1: Login with Correct Credentials ✅
```
Expected Result: Login successful, redirects to dashboard
Steps:
1. Visit http://localhost:8001/login.html
2. Enter username: admin
3. Enter password: admin123
4. Click "Sign In"
5. Should see loading animation
6. Should redirect to dashboard with data
7. Username "admin" should appear in top-right
```

### Test 2: Login with Wrong Password ✅
```
Expected Result: Error message shown, stay on login page
Steps:
1. Visit http://localhost:8001/login.html
2. Enter username: admin
3. Enter password: wrongpassword
4. Click "Sign In"
5. Should see red error message
6. Should stay on login page
7. Username should NOT be saved
```

### Test 3: Dashboard Access Control ✅
```
Expected Result: Cannot access dashboard without login
Steps:
1. Clear browser cookies/storage (DevTools > Application > Clear Site Data)
2. Try to visit http://localhost:8001/index.html directly
3. Should automatically redirect to login page
```

### Test 4: Logout Functionality ✅
```
Expected Result: Clears session and returns to login
Steps:
1. Login with admin/admin123
2. Dashboard should load
3. Click "Logout" button (bottom of sidebar)
4. Should be redirected to login page
5. Browser back button should not return to dashboard
```

### Test 5: Session Persistence ✅
```
Expected Result: Refresh page stays logged in
Steps:
1. Login to dashboard
2. Press F5 (refresh page)
3. Should stay on dashboard (not redirected to login)
4. All data should still be visible
5. Username still visible in header
```

### Test 6: Admin Panel ✅
```
Expected Result: Can access Django admin
Steps:
1. Go to http://localhost:8000/admin/
2. Login with: admin / admin123
3. Should see Django admin interface
4. Can view all models and data
```

---

## API Endpoints Reference

### Authentication
```
POST /api/login/
  Body: {"username": "admin", "password": "admin123"}
  Response: {"success": true, "user": {...}}

POST /api/logout/
  Response: {"success": true}
```

### Data Endpoints (All GET/POST/PUT/DELETE available)
```
/api/suppliers/
/api/products/
/api/warehouses/
/api/inventory-locations/
/api/movements/
/api/quality-control/
/api/purchase-orders/
/api/sales-orders/
/api/sales-analytics/
/api/forecasts/
```

---

## Troubleshooting

### Problem: "Connection error" on login
**Solution:**
1. Make sure Django server is running on port 8000
2. Make sure frontend server is running on port 8001
3. Check firewall isn't blocking connections
4. Try: `curl http://localhost:8000/api/login/` in another terminal

### Problem: Dashboard shows but no data
**Solution:**
1. Check browser console (F12) for errors
2. Check Network tab for failed API calls
3. Verify user is stored in localStorage (F12 > Application > localStorage)
4. Make sure both servers are running

### Problem: Logout button doesn't work
**Solution:**
1. Open DevTools console (F12)
2. Check for JavaScript errors
3. Try clicking again
4. Refresh page if stuck
5. Clear localStorage manually and try logging in again

### Problem: "Invalid username or password" error
**Solution:**
1. Verify you're using exactly: admin / admin123
2. Check CAPS LOCK is off
3. Make sure there are no extra spaces
4. Reset admin password in Django:
   ```python
   python manage.py shell
   from django.contrib.auth import get_user_model
   User = get_user_model()
   user = User.objects.get(username='admin')
   user.set_password('admin123')
   user.save()
   ```

### Problem: Can't connect to backend from frontend
**Solution:**
1. Check CORS settings in `backend/inventory_system/settings.py`
2. Should have `localhost:8001` in `CORS_ALLOWED_ORIGINS`
3. Restart Django server after changing settings
4. Check firewall: `netstat -ano | findstr :8000`

---

## File Locations

```
INVENTORY/
├── backend/
│   ├── inventory_system/
│   │   ├── settings.py          (Django config, CORS settings)
│   │   ├── urls.py              (Login routes configured here)
│   │   └── wsgi.py
│   ├── inventory_app/
│   │   ├── auth_views.py        (NEW - Login endpoint)
│   │   ├── views.py             (40+ API endpoints)
│   │   ├── models.py            (10 database models)
│   │   └── urls.py
│   ├── manage.py
│   └── db.sqlite3               (Database)
│
└── frontend/
    ├── login.html               (Login form page)
    ├── index.html               (Dashboard)
    └── assets/
        ├── css/
        │   └── style.css
        └── js/
            ├── app.js           (Main app, auth check)
            ├── auth.js          (Session management)
            ├── api.js           (API calls)
            ├── ui.js            (UI functions)
            └── config.js        (Configuration)
```

---

## Database Info

**Type:** SQLite (db.sqlite3)
**Location:** `backend/db.sqlite3`

**Admin Account:**
- Username: `admin`
- Password: `admin123`
- Email: `admin@inventory.com`
- Status: Superuser & Staff

**Sample Data Created:**
- 2 suppliers
- 5 products
- 2 warehouses
- Various inventory locations
- Purchase and sales orders

---

## Frontend Server Details

**Location:** `http://localhost:8001/`
**Running:** Python's built-in HTTP server
**Start Command:** `python -m http.server 8001` (from frontend folder)

**Files Served:**
- `login.html` - Login page
- `index.html` - Main dashboard
- `assets/` - CSS, JavaScript, images

---

## Backend Server Details

**Location:** `http://localhost:8000/`
**Framework:** Django 4.2.0
**Database:** SQLite
**API Framework:** Django REST Framework 3.14.0
**Start Command:** `python manage.py runserver` (from backend folder)

**Features:**
- 10 database models
- 40+ API endpoints
- Admin panel at `/admin/`
- CORS enabled
- Authentication endpoint at `/api/login/`

---

## Performance Notes

- Database queries optimized with select_related()
- API responses paginated (20 items per page)
- Chart.js used for visualizations
- CSS and JS minified where possible
- Assets served with relative paths

---

## Security Reminders

⚠️ This is a development setup. For production:
1. Change DEBUG = False in settings.py
2. Set a strong SECRET_KEY
3. Remove @csrf_exempt from auth_views.py
4. Implement proper authentication (JWT)
5. Use HTTPS
6. Set up proper database (PostgreSQL)
7. Configure allowed hosts properly
8. Add rate limiting
9. Implement proper logging
10. Use environment variables for secrets

---

## Contact & Support

All systems are fully functional and tested.

**Current Status:** ✅ COMPLETE AND OPERATIONAL

For any issues:
1. Check this guide for troubleshooting steps
2. Review browser console (F12) for errors
3. Check terminal output where servers are running
4. Review Django logs for server-side errors

---

Generated: 2024
Status: Production Ready (Development Mode)
