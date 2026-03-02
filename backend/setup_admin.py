#!/usr/bin/env python
"""Setup admin user for testing"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_system.settings')
django.setup()

from django.contrib.auth.models import User

# Check if admin already exists
if User.objects.filter(username='admin').exists():
    print("Admin user already exists!")
    admin = User.objects.get(username='admin')
    print(f"Username: {admin.username}")
    print(f"Email: {admin.email}")
else:
    # Create admin user
    admin = User.objects.create_user(
        username='admin',
        email='admin@inventory.com',
        password='admin'
    )
    print("Admin user created successfully!")
    print(f"Username: {admin.username}")
    print(f"Email: {admin.email}")
    print("Password: admin")
