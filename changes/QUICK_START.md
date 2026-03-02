# Quick Start Guide - Inventory Management System

## 1. First Time Setup (5 minutes)

### Step 1: Clone and Navigate
```bash
cd INVENTORY
```

### Step 2: Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Copy .env template
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

### Step 3: Setup Database
```bash
# Make sure PostgreSQL is running
# Create the database and run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

### Step 4: Start Backend
```bash
python manage.py runserver
```

### Step 5: Start Frontend (in new terminal)
```bash
cd frontend
python -m http.server 8001
```

### Step 6: Access Application
- **Dashboard:** http://localhost:8001
- **Admin:** http://localhost:8000/admin
- **API:** http://localhost:8000/api

---

## 2. Daily Usage

### Start Development Servers
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
python -m http.server 8001
```

### Create Sample Data
```bash
python manage.py shell

# In the Django shell:
from inventory_app.models import *
from django.contrib.auth.models import User

# Create a user if needed
user = User.objects.create_user(username='test', password='test')

# Create suppliers
supplier = Supplier.objects.create(
    name='Acme Corp',
    email='contact@acme.com',
    phone='123-456-7890',
    address='123 Business St',
    city='New York',
    country='USA'
)

# Create products
product = Product.objects.create(
    barcode='123456789',
    name='Sample Product',
    description='A test product',
    category='electronics',
    supplier=supplier,
    unit_cost=10.00,
    unit_price=25.00,
    reorder_level=50
)

# Create warehouse
warehouse = Warehouse.objects.create(
    name='Main Warehouse',
    address='456 Storage Ave',
    city='New York',
    country='USA',
    manager_name='John Doe',
    manager_phone='555-1234',
    capacity=1000
)

# Create inventory location
location = InventoryLocation.objects.create(
    warehouse=warehouse,
    product=product,
    aisle='A',
    rack='1',
    shelf='1',
    bin='1',
    quantity=100,
    batch_number='BATCH001'
)

# Exit shell
exit()
```

---

## 3. Key Features Quick Reference

### 1. Search Products by Barcode
1. Click "Scan Barcode" button in Products section
2. Enter or scan the barcode
3. Product details will appear instantly

### 2. Create Purchase Order
1. Go to "Purchase Orders" section
2. Click "Create PO"
3. Select supplier and product
4. Enter quantity and delivery date
5. Submit

### 3. Create Sales Order
1. Go to "Sales Orders" section
2. Click "Create SO"
3. Select product
4. Enter customer details and quantity
5. Submit

### 4. Generate Forecasts
1. Go to "Forecasts" section
2. Click "Generate Forecast"
3. Select product and days ahead
4. View predictions

### 5. Export Data
1. Any table has an "Export" button
2. Choose format (CSV, PDF, or XLSX)
3. File downloads automatically

### 6. View Reports
1. Go to "Reports & Analytics"
2. Click on desired report type
3. View chart or data table
4. Export if needed

---

## 4. API Usage Examples

### Get All Products
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/products/
```

### Create Product
```bash
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "barcode": "NEW123",
    "name": "New Product",
    "description": "Test",
    "category": "electronics",
    "supplier": 1,
    "unit_cost": 10,
    "unit_price": 25,
    "reorder_level": 50
  }' \
  http://localhost:8000/api/products/
```

### Lookup by Barcode
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/products/barcode_lookup/?barcode=123456789
```

### Get Low Stock Products
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/products/low_stock/
```

### Export as CSV
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/products/export_csv/ > products.csv
```

---

## 5. Common Issues & Solutions

### Issue: "No such table" error
**Solution:** Run migrations
```bash
python manage.py migrate
```

### Issue: Database connection error
**Solution:** Check PostgreSQL is running
```bash
# Windows
net start PostgreSQL14

# macOS
brew services start postgresql
```

### Issue: Port already in use
**Solution:** Use different port
```bash
python manage.py runserver 8002
python -m http.server 8003  # for frontend
```

### Issue: CORS errors in console
**Solution:** Check API URL in frontend is correct (http://localhost:8000/api)

### Issue: Login not working
**Solution:** Check token is being stored in localStorage

---

## 6. Admin Panel

Access admin panel: http://localhost:8000/admin

You can:
- Manage users and permissions
- View/edit all database records
- Perform bulk operations
- Add test data

---

## 7. Database Backup

### Backup PostgreSQL Database
```bash
# Create backup
pg_dump -U postgres inventory_db > backup.sql

# Restore from backup
psql -U postgres inventory_db < backup.sql
```

---

## 8. Development Tips

### Enable Debug Toolbar
```python
# In settings.py, add to INSTALLED_APPS
'debug_toolbar',
```

### View SQL Queries
```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as ctx:
    # Your code here
    pass

for query in ctx.captured_queries:
    print(query['sql'])
```

### Clear Cache
```bash
python manage.py clear_cache
```

### Create Data Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 9. Performance Optimization

### Enable Query Caching
```python
# In settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

### Add Database Indexes
Already configured in models for commonly searched fields

### Use Pagination
All list endpoints support pagination with ?page parameter

---

## 10. Next Steps

1. **Customize UI:** Modify `frontend/assets/css/style.css`
2. **Add More Features:** Extend models in `backend/inventory_app/models.py`
3. **Deploy:** Follow production deployment guide in README.md
4. **Add Tests:** Write tests in `backend/inventory_app/tests.py`
5. **Monitor:** Set up monitoring with Django Debug Toolbar or Sentry

---

## Support & Help

- Check README.md for detailed documentation
- Review API endpoints in README.md
- Check browser console for JavaScript errors
- Check Django server logs for backend errors
- Visit Django documentation: https://docs.djangoproject.com/
