#!/usr/bin/env python
"""
Sample data creation script for Inventory Management System
Run with: python manage.py shell < create_sample_data.py
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_system.settings')
django.setup()

from django.contrib.auth.models import User
from inventory_app.models import Supplier, Product, Warehouse, InventoryLocation, Movement, PurchaseOrder, SalesOrder, SalesAnalytics, Forecast
from django.utils import timezone
from datetime import timedelta

# Clear existing data
print("Creating sample data...")

# Create suppliers
suppliers = [
    Supplier.objects.create(
        name="TechSupply Co",
        email="contact@techsupply.com",
        phone="+1-555-0101",
        address="123 Tech Street",
        city="San Francisco",
        country="USA"
    ),
    Supplier.objects.create(
        name="Global Imports Ltd",
        email="info@globalimports.com",
        phone="+1-555-0102",
        address="456 Trade Ave",
        city="New York",
        country="USA"
    ),
]
print(f"✓ Created {len(suppliers)} suppliers")

# Create products
products = [
    Product.objects.create(
        name="Laptop Pro X1",
        barcode="TECH-001",
        category="Electronics",
        unit_cost=800,
        unit_price=1200,
        reorder_level=5,
        status="active",
        supplier=suppliers[0]
    ),
    Product.objects.create(
        name="USB-C Cable 3m",
        barcode="TECH-002",
        category="Accessories",
        unit_cost=5,
        unit_price=12,
        reorder_level=50,
        status="active",
        supplier=suppliers[0]
    ),
    Product.objects.create(
        name="Monitor 27 inch",
        barcode="TECH-003",
        category="Electronics",
        unit_cost=250,
        unit_price=400,
        reorder_level=3,
        status="active",
        supplier=suppliers[1]
    ),
    Product.objects.create(
        name="Keyboard Mechanical",
        barcode="TECH-004",
        category="Peripherals",
        unit_cost=100,
        unit_price=180,
        reorder_level=10,
        status="active",
        supplier=suppliers[1]
    ),
    Product.objects.create(
        name="Mouse Wireless",
        barcode="TECH-005",
        category="Peripherals",
        unit_cost=25,
        unit_price=50,
        reorder_level=20,
        status="active",
        supplier=suppliers[0]
    ),
]
print(f"✓ Created {len(products)} products")

# Create warehouses
warehouses = [
    Warehouse.objects.create(
        name="Main Warehouse",
        address="789 Storage Lane",
        city="San Francisco",
        country="USA",
        manager_name="John Smith",
        capacity=10000
    ),
    Warehouse.objects.create(
        name="East Coast Hub",
        address="321 Warehouse Blvd",
        city="New York",
        country="USA",
        manager_name="Jane Doe",
        capacity=5000
    ),
]
print(f"✓ Created {len(warehouses)} warehouses")

# Create inventory locations
for product in products:
    for warehouse in warehouses:
        InventoryLocation.objects.create(
            product=product,
            warehouse=warehouse,
            aisle=f"A{product.id}",
            rack=f"R{warehouse.id}",
            shelf="1",
            bin=f"B{product.id}{warehouse.id}",
            quantity=50 + (product.id * 10),
            batch_number=f"BATCH-{product.id}",
            expiry_date=timezone.now().date() + timedelta(days=365)
        )
print(f"✓ Created {len(products) * len(warehouses)} inventory locations")

# Create purchase orders
user = User.objects.first() or User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)

for i, product in enumerate(products[:3]):
    PurchaseOrder.objects.create(
        po_number=f"PO-2026-{1000+i}",
        supplier=suppliers[i % 2],
        product=product,
        quantity=100,
        unit_cost=product.unit_cost,
        total_cost=100 * product.unit_cost,
        status="draft" if i == 0 else "received",
        expected_delivery=timezone.now().date() + timedelta(days=7),
        created_by=user
    )
print(f"✓ Created purchase orders")

# Create sales orders and analytics
today = timezone.now().date()
for i, product in enumerate(products):
    # Create sales order
    SalesOrder.objects.create(
        so_number=f"SO-2026-{2000+i}",
        product=product,
        quantity=10,
        unit_price=product.unit_price,
        total_price=10 * product.unit_price,
        customer_name=f"Customer {i+1}",
        customer_email=f"customer{i+1}@example.com",
        customer_phone="+1-555-0200",
        status="pending",
        ship_date=today + timedelta(days=3),
        created_by=user
    )
    
    # Create sales analytics for last 30 days
    for j in range(30):
        date = today - timedelta(days=j)
        SalesAnalytics.objects.get_or_create(
            product=product,
            date=date,
            defaults={
                'units_sold': 5 + j % 10,
                'revenue': (5 + j % 10) * product.unit_price
            }
        )

print(f"✓ Created sales orders and analytics")

# Create forecasts
for product in products:
    for i in range(1, 31):
        forecast_date = today + timedelta(days=i)
        Forecast.objects.get_or_create(
            product=product,
            forecast_date=forecast_date,
            defaults={
                'predicted_demand': 10 + (i % 15),
                'confidence_score': 0.75
            }
        )

print(f"✓ Created forecasts")
print("\n✅ All sample data created successfully!")
print("\nYou can now:")
print("1. Access the dashboard at http://localhost:8001")
print("2. Browse API at http://localhost:8000/api/")
print("3. Use the admin panel at http://localhost:8000/admin/")
