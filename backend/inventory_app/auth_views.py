from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import FileResponse, HttpResponse
from django.http import FileResponse
from django.utils import timezone
import json
import os
from pathlib import Path

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    User login endpoint
    Expects: {"username": "admin", "password": "admin123"}
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Return success with user information
            return Response({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    except json.JSONDecodeError:
        return Response(
            {'error': 'Invalid JSON'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    """
    User logout endpoint
    """
    return Response({
        'success': True,
        'message': 'Logged out successfully'
    }, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint
    """
    return Response({
        'status': 'ok',
        'message': 'Inventory Management System is running',
        'version': '1.0.0',
        'timestamp': timezone.now().isoformat()
    }, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token(request):
    """
    Verify if a user is authenticated (for frontend validation)
    Expects: {"user_id": 1} or just checks if request has auth
    """
    try:
        # Frontend sends user data, we just validate it exists
        data = request.body if request.body else b'{}'
        user_data = json.loads(data) if data else {}
        
        if not user_data.get('user_id'):
            return Response({
                'authenticated': False,
                'message': 'Not authenticated'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # User exists in localStorage, frontend is authenticated
        return Response({
            'authenticated': True,
            'user_id': user_data.get('user_id'),
            'message': 'User is authenticated'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'authenticated': False,
            'error': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    User signup/registration endpoint
    Expects: {"username": "newuser", "email": "user@example.com", "password": "password123", "password_confirm": "password123"}
    """
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        password_confirm = data.get('password_confirm', '').strip()

        # Validation
        if not username or not email or not password or not password_confirm:
            return Response(
                {'error': 'All fields are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if passwords match
        if password != password_confirm:
            return Response(
                {'error': 'Passwords do not match'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Password length validation
        if len(password) < 6:
            return Response(
                {'error': 'Password must be at least 6 characters long'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Email already registered'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Return success with user information
        return Response({
            'success': True,
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser
            }
        }, status=status.HTTP_201_CREATED)

    except json.JSONDecodeError:
        return Response(
            {'error': 'Invalid JSON'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# HTML File Serving Views
@require_http_methods(["GET"])
def serve_login(request):
    """Serve login.html"""
    try:
        frontend_dir = os.path.join(Path(__file__).resolve().parent.parent.parent, 'frontend')
        login_file = os.path.join(frontend_dir, 'login.html')
        
        if not os.path.exists(login_file):
            return Response(
                {'error': f'login.html not found at {login_file}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Read file content as string
        with open(login_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return HttpResponse(content, content_type='text/html')
    except Exception as e:
        return Response(
            {'error': f'Error serving login page: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@require_http_methods(["GET"])
def serve_signup(request):
    """Serve signup.html"""
    try:
        frontend_dir = os.path.join(Path(__file__).resolve().parent.parent.parent, 'frontend')
        signup_file = os.path.join(frontend_dir, 'signup.html')
        
        if not os.path.exists(signup_file):
            return Response(
                {'error': f'signup.html not found at {signup_file}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Read file content as string
        with open(signup_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return HttpResponse(content, content_type='text/html')
    except Exception as e:
        return Response(
            {'error': f'Error serving signup page: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@require_http_methods(["GET"])
def serve_dashboard(request):
    """Serve index.html (dashboard)"""
    try:
        frontend_dir = os.path.join(Path(__file__).resolve().parent.parent.parent, 'frontend')
        index_file = os.path.join(frontend_dir, 'index.html')
        
        if not os.path.exists(index_file):
            from django.http import HttpResponseNotFound
            return HttpResponseNotFound(f'index.html not found at {index_file}')
        
        # Read file content as string
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return HttpResponse(content, content_type='text/html')
    except Exception as e:
        from django.http import HttpResponseServerError
        return HttpResponseServerError(f'Error serving dashboard: {str(e)}')


# ===== STATIC ASSETS SERVING =====

@require_http_methods(["GET"])
def serve_css(request, filename):
    """Serve CSS files from frontend/assets/css/"""
    try:
        frontend_dir = os.path.join(Path(__file__).resolve().parent.parent.parent, 'frontend')
        css_file = os.path.join(frontend_dir, 'assets', 'css', filename)
        
        if not os.path.exists(css_file):
            from django.http import HttpResponseNotFound
            return HttpResponseNotFound(f'CSS file not found: {filename}')
        
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return HttpResponse(content, content_type='text/css')
    except Exception as e:
        from django.http import HttpResponseServerError
        return HttpResponseServerError(f'Error serving CSS: {str(e)}')


@require_http_methods(["GET"])
def serve_js(request, filename):
    """Serve JavaScript files from frontend/assets/js/"""
    try:
        frontend_dir = os.path.join(Path(__file__).resolve().parent.parent.parent, 'frontend')
        js_file = os.path.join(frontend_dir, 'assets', 'js', filename)
        
        if not os.path.exists(js_file):
            from django.http import HttpResponseNotFound
            return HttpResponseNotFound(f'JS file not found: {filename}')
        
        with open(js_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return HttpResponse(content, content_type='application/javascript')
    except Exception as e:
        from django.http import HttpResponseServerError
        return HttpResponseServerError(f'Error serving JS: {str(e)}')


@require_http_methods(["GET"])
def serve_asset(request, filepath):
    """Serve general assets from frontend/assets/"""
    try:
        frontend_dir = os.path.join(Path(__file__).resolve().parent.parent.parent, 'frontend')
        asset_file = os.path.join(frontend_dir, 'assets', filepath)
        
        # Security: prevent directory traversal
        if not os.path.abspath(asset_file).startswith(os.path.abspath(os.path.join(frontend_dir, 'assets'))):
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden('Access denied')
        
        if not os.path.exists(asset_file):
            from django.http import HttpResponseNotFound
            return HttpResponseNotFound(f'Asset not found: {filepath}')
        
        # Determine content type
        if filepath.endswith('.css'):
            content_type = 'text/css'
        elif filepath.endswith('.js'):
            content_type = 'application/javascript'
        elif filepath.endswith('.json'):
            content_type = 'application/json'
        elif filepath.endswith('.png'):
            content_type = 'image/png'
        elif filepath.endswith('.jpg') or filepath.endswith('.jpeg'):
            content_type = 'image/jpeg'
        elif filepath.endswith('.gif'):
            content_type = 'image/gif'
        elif filepath.endswith('.svg'):
            content_type = 'image/svg+xml'
        else:
            content_type = 'application/octet-stream'
        
        with open(asset_file, 'rb') as f:
            content = f.read()
        
        return HttpResponse(content, content_type=content_type)
    except Exception as e:
        from django.http import HttpResponseServerError
        return HttpResponseServerError(f'Error serving asset: {str(e)}')
