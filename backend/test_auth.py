#!/usr/bin/env python
"""Test authentication directly"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_system.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Test directly
admin = User.objects.get(username='admin')
print(f"User found: {admin.username}")
print(f"Email: {admin.email}")
print(f"Password hash: {admin.password}")

# Test authentication
user = authenticate(username='admin', password='admin')
if user is not None:
    print("\nAuthentication: SUCCESS")
else:
    print("\nAuthentication: FAILED")
    
    # Try to understand why
    from django.contrib.auth.hashers import make_password, check_password
    test_hash = make_password('admin')
    print(f"\nTest hash for 'admin': {test_hash}")
    print(f"Stored hash matches: {check_password('admin', admin.password)}")
