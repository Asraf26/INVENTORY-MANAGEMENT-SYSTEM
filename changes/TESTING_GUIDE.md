# Testing Guide - Inventory Management System

## Unit Testing

### Run All Tests
```bash
cd backend
python manage.py test
```

### Run Specific Test
```bash
python manage.py test inventory_app.tests.SupplierTest
```

### Run with Verbosity
```bash
python manage.py test --verbosity=2
```

## Test Examples

### Sample Test File: inventory_app/tests.py
```python
from django.test import TestCase
from django.contrib.auth.models import User
from inventory_app.models import Supplier, Product, Warehouse, InventoryLocation

class SupplierTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            email='test@supplier.com',
            phone='123-456-7890',
            address='Test Address',
            city='Test City',
            country='Test Country'
        )

    def test_supplier_creation(self):
        self.assertEqual(self.supplier.name, 'Test Supplier')
        self.assertEqual(Supplier.objects.count(), 1)

    def test_supplier_str(self):
        self.assertEqual(str(self.supplier), 'Test Supplier')

class ProductTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            email='test@supplier.com',
            phone='123-456-7890',
            address='Test Address',
            city='Test City',
            country='Test Country'
        )
        self.product = Product.objects.create(
            barcode='123456789',
            name='Test Product',
            description='Test Description',
            category='electronics',
            supplier=self.supplier,
            unit_cost=10.00,
            unit_price=25.00,
            reorder_level=50
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.barcode, '123456789')

    def test_product_pricing(self):
        self.assertEqual(self.product.unit_cost, 10.00)
        self.assertEqual(self.product.unit_price, 25.00)

class WarehouseTest(TestCase):
    def setUp(self):
        self.warehouse = Warehouse.objects.create(
            name='Test Warehouse',
            address='Test Address',
            city='Test City',
            country='Test Country',
            manager_name='John Doe',
            manager_phone='555-1234',
            capacity=1000
        )

    def test_warehouse_creation(self):
        self.assertEqual(self.warehouse.name, 'Test Warehouse')
        self.assertEqual(self.warehouse.capacity, 1000)

class InventoryLocationTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            email='test@supplier.com',
            phone='123-456-7890',
            address='Test Address',
            city='Test City',
            country='Test Country'
        )
        self.product = Product.objects.create(
            barcode='123456789',
            name='Test Product',
            description='Test Description',
            category='electronics',
            supplier=self.supplier,
            unit_cost=10.00,
            unit_price=25.00,
            reorder_level=50
        )
        self.warehouse = Warehouse.objects.create(
            name='Test Warehouse',
            address='Test Address',
            city='Test City',
            country='Test Country',
            manager_name='John Doe',
            manager_phone='555-1234',
            capacity=1000
        )
        self.location = InventoryLocation.objects.create(
            warehouse=self.warehouse,
            product=self.product,
            aisle='A',
            rack='1',
            shelf='1',
            bin='1',
            quantity=100
        )

    def test_inventory_location_creation(self):
        self.assertEqual(self.location.quantity, 100)
        self.assertEqual(self.location.aisle, 'A')
```

## API Testing

### Using cURL

#### Test Product Search
```bash
curl -X GET \
  -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/products/?search=laptop"
```

#### Test Barcode Lookup
```bash
curl -X GET \
  -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/products/barcode_lookup/?barcode=123456789"
```

#### Test Export
```bash
curl -X GET \
  -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/products/export_csv/" \
  > products.csv
```

### Using Postman

1. Create new collection "Inventory API"
2. Add Authorization header: `Authorization: Bearer YOUR_TOKEN`
3. Create requests for each endpoint
4. Test different scenarios

## Frontend Testing

### Browser Console Testing

```javascript
// Test API call
apiGet(API_ENDPOINTS.products).then(data => console.log(data));

// Test notification
showSuccess('Test notification');

// Test search
apiSearch(API_ENDPOINTS.products, 'laptop');

// Test barcode lookup
lookupBarcode('123456789');
```

### Manual Testing Checklist

- [ ] Dashboard loads correctly
- [ ] All stats cards display correct counts
- [ ] Charts render properly
- [ ] Navigation between sections works
- [ ] Search functionality works
- [ ] Filters work correctly
- [ ] Add/Edit/Delete operations work
- [ ] Export buttons generate files
- [ ] Modals open and close properly
- [ ] Forms validate correctly
- [ ] Notifications display
- [ ] Logout works
- [ ] Responsive design works on mobile

## Performance Testing

### Load Testing with Apache Bench
```bash
# Test dashboard endpoint
ab -n 1000 -c 100 http://localhost:8000/api/products/

# Results show: requests/second, response time
```

### Database Query Performance
```bash
# In Django shell
from django.test.utils import CaptureQueriesContext
from django.db import connection

with CaptureQueriesContext(connection) as ctx:
    products = Product.objects.all()
    for p in products:
        print(p.name)

print(f"Queries executed: {len(ctx.captured_queries)}")
for query in ctx.captured_queries:
    print(query['time'])
```

## Security Testing

### SQL Injection Testing
```bash
# Try to inject SQL
curl "http://localhost:8000/api/products/?search=test' OR '1'='1"
# Should not return all products
```

### Authentication Testing
```bash
# Test without token
curl http://localhost:8000/api/products/

# Should return 401 Unauthorized
```

### CORS Testing
```bash
# From different domain
curl -H "Origin: http://different-domain.com" \
  -H "Access-Control-Request-Method: GET" \
  http://localhost:8000/api/products/
```

## Coverage Testing

### Install Coverage
```bash
pip install coverage
```

### Generate Coverage Report
```bash
coverage run --source='inventory_app' manage.py test
coverage report
coverage html
```

### View Coverage Report
Open `htmlcov/index.html` in browser

## Continuous Integration Setup

### GitHub Actions Example (.github/workflows/tests.yml)
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:12
        env:
          POSTGRES_DB: inventory_db
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    
    - name: Install dependencies
      run: |
        pip install -r backend/requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        python manage.py test
```

## Bug Reporting

### Create Bug Report
Include:
1. Browser/Environment
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Screenshots/logs

## Performance Optimization

### Database Query Optimization
```python
# Bad - N+1 query problem
for product in Product.objects.all():
    print(product.supplier.name)

# Good - Use select_related
for product in Product.objects.select_related('supplier'):
    print(product.supplier.name)
```

### Caching Example
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def get_products(request):
    return Response(ProductSerializer(
        Product.objects.all(), 
        many=True
    ).data)
```

## Debugging Tips

### Django Debug Toolbar
```python
# Add to INSTALLED_APPS in settings
'debug_toolbar',

# Add to MIDDLEWARE
'debug_toolbar.middleware.DebugToolbarMiddleware',

# Add to urlpatterns in urls.py
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
```

### Logging
```python
import logging

logger = logging.getLogger(__name__)

logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
```

## Performance Metrics

### Monitor Key Metrics
- Average response time: < 500ms
- Database query time: < 100ms
- API availability: > 99.5%
- Error rate: < 0.1%
- Cache hit rate: > 80%

---

Happy Testing! 🚀
