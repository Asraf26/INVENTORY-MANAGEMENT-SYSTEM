# How to Run the Project

## Quick Start (Copy & Paste)

### Step 1: Open PowerShell in Project Directory
```powershell
cd "c:\Users\asraf\Desktop\New folder (2)"
```

### Step 2: Activate Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` at the start of your terminal prompt.

### Step 3: Navigate to Backend
```powershell
cd backend
```

### Step 4: Run Django Server
```powershell
python manage.py runserver
```
ipconfig
You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## Access the Application

Once server is running:

1. **Open Browser** → `http://localhost:8000/login.html`
2. **Login with:**
   - Username: `admin`
   - Password: `admin`
3. **See Dashboard** → Full dashboard with CSS styling

---

## Complete Step-by-Step

### If PowerShell Blocks Script Execution

If you get execution policy error, run this once:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activation again.

### Manual Activation (Windows Alternative)

Instead of `.venv\Scripts\Activate.ps1`, use:
```powershell
.\.venv\Scripts\activate.bat
```

---

## Full Sequence (One Command Block)

Copy all at once:
```powershell
cd "c:\Users\asraf\Desktop\New folder (2)"; .\.venv\Scripts\Activate.ps1; cd backend; python manage.py runserver
```

---

## Stop the Server

Press `CTRL + BREAK` (or `CTRL + C`) to stop the server.

---

## Troubleshooting

### Server won't start
- Make sure port 8000 is not in use
- Close any other Django processes
- Try: `netstat -ano | findstr 8000`

### Can't login
- Database might need reset
- Run: `python manage.py migrate`
- Create admin user: `python manage.py createsuperuser`
- Use admin/admin credentials

### CSS/JS not loading
- Make sure server is running
- Clear browser cache (CTRL + SHIFT + Delete)
- Hard refresh (CTRL + SHIFT + R)

### Virtual environment issues
- Reinstall: `python -m venv .venv`
- Then activate and run: `pip install -r requirements.txt`

---

## File Locations (For Reference)

```
Project Root: c:\Users\asraf\Desktop\New folder (2)\
├── backend/              (Django server files)
│   ├── manage.py         (Django commands)
│   ├── db.sqlite3        (Database)
│   └── requirements.txt  (Dependencies)
├── frontend/             (Web interface)
│   ├── index.html        (Dashboard)
│   ├── login.html        (Login page)
│   ├── assets/
│   │   ├── css/style.css (Styling)
│   │   └── js/           (JavaScript files)
└── .venv/                (Virtual environment)
```

---

## Database Reset (if needed)

```powershell
# Delete existing database
Remove-Item backend\db.sqlite3

# Create new database
cd backend
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# username: admin
# password: admin
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| **Start Project** | `cd "c:\Users\asraf\Desktop\New folder (2)"; .\.venv\Scripts\Activate.ps1; cd backend; python manage.py runserver` |
| **Stop Server** | `CTRL + BREAK` |
| **Activate Env** | `.\.venv\Scripts\Activate.ps1` |
| **Install Deps** | `pip install -r requirements.txt` |
| **Run Migrations** | `python manage.py migrate` |
| **Create Admin** | `python manage.py createsuperuser` |
| **Reset DB** | Delete `db.sqlite3` then run `migrate` |
| **Test CSS/JS** | Open browser console (F12) and check for 200 status |

---

## Tips

✓ Always activate `.venv` before running commands
✓ Always run `python manage.py runserver` from `/backend` directory
✓ Default URL is `http://localhost:8000/`
✓ Login page is at `http://localhost:8000/login.html`
✓ Dashboard is at `http://localhost:8000/index.html` (after login)
✓ Press `CTRL + BREAK` to stop server, not just `CTRL + C`

---

## What Happens When You Run It

1. ✓ Django starts on port 8000
2. ✓ Static assets (CSS, JS) load from custom routes
3. ✓ Login page displays with styling
4. ✓ Authentication system active
5. ✓ Dashboard accessible after login
6. ✓ All features ready to use

---

**That's it! Your project will be running and ready to use.**
