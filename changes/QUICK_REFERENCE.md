# ⚡ Quick Reference Card

## 🚀 Start Application (2 Terminal Windows)

### Terminal 1 - Backend
```powershell
cd c:\Users\asraf\Desktop\INVENTORY\backend
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```
Wait for: `Starting development server at http://127.0.0.1:8000/`

### Terminal 2 - Frontend
```powershell
cd c:\Users\asraf\Desktop\INVENTORY\frontend
python -m http.server 8001
```
Wait for: `Serving HTTP on 0.0.0.0 port 8001`

### Open Browser
```
http://localhost:8001/login.html
```

---

## 🔐 Login

**Username:** `admin`
**Password:** `admin123`

Click "Sign In" → Redirects to dashboard

---

## 📍 URLs

| Page | URL |
|------|-----|
| Login | http://localhost:8001/login.html |
| Dashboard | http://localhost:8001/index.html |
| Admin Panel | http://localhost:8000/admin/ |
| API Docs | http://localhost:8000/api/ |

---

## 🔧 Key Features

✅ Login with credential validation
✅ Dashboard with 9 sections
✅ 40+ API endpoints
✅ Session management (logout)
✅ Access control
✅ Data visualization (Chart.js)
✅ Responsive design

---

## 📂 Important Files

**Backend:**
- `backend/inventory_app/auth_views.py` - Login endpoint
- `backend/inventory_system/urls.py` - Routes
- `backend/db.sqlite3` - Database

**Frontend:**
- `frontend/login.html` - Login page
- `frontend/index.html` - Dashboard
- `frontend/assets/js/app.js` - Main app logic
- `frontend/assets/css/style.css` - Styling

---

## ✅ Testing

**Test Login:**
1. Enter: admin / admin123
2. Should redirect to dashboard
3. Username shows in top-right

**Test Logout:**
1. Click "Logout" button (sidebar)
2. Should redirect to login page

**Test Access Control:**
1. Clear browser storage (DevTools > Application > Clear)
2. Try to visit http://localhost:8001/index.html
3. Should redirect to login.html

---

## 🐛 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Connection error | Verify Django running on port 8000 |
| No data shown | Check browser console (F12), verify API calls |
| CSS not loading | Check frontend server running on port 8001 |
| Stuck on login | Clear localStorage, try again |
| Admin login fails | Verify credentials: admin / admin123 |

---

## 🔌 API Examples

### Login
```bash
POST http://localhost:8000/api/login/
Body: {"username": "admin", "password": "admin123"}
```

### Get Products
```bash
GET http://localhost:8000/api/products/
```

### Get Suppliers
```bash
GET http://localhost:8000/api/suppliers/
```

---

## 📊 Data in Database

- **Suppliers:** 2
- **Products:** 5
- **Warehouses:** 2
- **Admin User:** admin / admin123

---

## 📚 Documentation

1. **RUNNING_AND_TESTING_GUIDE.md** - Full setup & testing guide
2. **AUTHENTICATION_CHANGES.md** - Authentication details
3. **SYSTEM_STATUS.md** - Current system status
4. **LOGIN_SYSTEM_COMPLETE.md** - Login features

---

## ⏱️ Expected Load Times

- Login page: < 1 second
- Dashboard: 1-2 seconds
- API call: 50-200ms
- Data refresh: Instant

---

## 🎯 Next Actions

1. ✅ Start both servers
2. ✅ Go to http://localhost:8001/login.html
3. ✅ Login with admin / admin123
4. ✅ Explore dashboard features
5. ✅ Test logout

---

## ℹ️ System Info

- **Backend:** Django 4.2.0 on port 8000
- **Frontend:** Python HTTP Server on port 8001
- **Database:** SQLite (db.sqlite3)
- **Framework:** Django REST Framework 3.14.0
- **Status:** ✅ FULLY OPERATIONAL

---

**All systems ready! Start the servers and begin using the system.** 🎉

Questions? Check the documentation files or review browser console for details.
