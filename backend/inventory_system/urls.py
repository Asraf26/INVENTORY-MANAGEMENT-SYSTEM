"""
URL configuration for inventory_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from inventory_app.auth_views import (
    login, logout, signup, 
    serve_login, serve_signup, serve_dashboard,
    health_check, verify_token,
    serve_css, serve_js, serve_asset
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # HTML Pages
    path('login.html', serve_login, name='login_page'),
    path('signup.html', serve_signup, name='signup_page'),
    path('index.html', serve_dashboard, name='dashboard_page'),
    path('', serve_login, name='home'),  # Default to login page
    
    # Static Assets
    path('assets/css/<str:filename>', serve_css, name='serve_css'),
    path('assets/js/<str:filename>', serve_js, name='serve_js'),
    path('assets/<path:filepath>', serve_asset, name='serve_asset'),
    
    # API Endpoints - Authentication
    path('api/login/', login, name='api_login'),
    path('api/signup/', signup, name='api_signup'),
    path('api/logout/', logout, name='api_logout'),
    path('api/health/', health_check, name='api_health'),
    path('api/verify-token/', verify_token, name='api_verify_token'),
    
    # API Endpoints - Other
    path('api/', include('inventory_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
