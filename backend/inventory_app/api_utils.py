"""
API Response Utilities Module
Provides consistent error handling and response formatting for all API endpoints
This ensures predictable error responses across the application

Usage:
    from .api_utils import APIResponse, validate_required_fields
    
    def some_api_view(request):
        # Validate input
        required = {'field1', 'field2'}
        errors = validate_required_fields(request.data, required)
        if errors:
            return APIResponse.error('Validation failed', errors=errors, status=400)
        
        # Process request
        try:
            # ... your logic
            return APIResponse.success(data, 'Success message')
        except Exception as e:
            return APIResponse.error(str(e), context='operation_context')
"""

from rest_framework.response import Response
from rest_framework import status as http_status


class APIResponse:
    """
    Standardized API response format
    
    Success Format:
    {
        "success": true,
        "message": "Operation successful",
        "data": { ... }
    }
    
    Error Format:
    {
        "success": false,
        "message": "Error description",
        "errors": { "field": "error message" },
        "status": 400
    }
    """

    @staticmethod
    def success(data=None, message='Success', status=http_status.HTTP_200_OK):
        """
        Return a success response
        
        Args:
            data: Response payload
            message: Success message
            status: HTTP status code
        
        Returns:
            Response object
        """
        response_data = {
            'success': True,
            'message': message
        }
        
        if data is not None:
            response_data['data'] = data
        
        return Response(response_data, status=status)

    @staticmethod
    def error(message='An error occurred', errors=None, status=http_status.HTTP_400_BAD_REQUEST, context=None):
        """
        Return an error response
        
        Args:
            message: Error description
            errors: Dictionary of field-level errors
            status: HTTP status code
            context: Optional context for debugging
        
        Returns:
            Response object
        """
        response_data = {
            'success': False,
            'message': message
        }
        
        if errors and isinstance(errors, dict):
            response_data['errors'] = errors
        
        if context:
            response_data['context'] = context
        
        return Response(response_data, status=status)

    @staticmethod
    def validation_error(errors, message='Validation failed'):
        """
        Return a validation error response
        
        Args:
            errors: Dictionary of field-level errors
            message: Custom error message
        
        Returns:
            Response object
        """
        return APIResponse.error(
            message=message,
            errors=errors,
            status=http_status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def not_found(message='Resource not found'):
        """
        Return a 404 not found response
        
        Args:
            message: Error message
        
        Returns:
            Response object
        """
        return APIResponse.error(
            message=message,
            status=http_status.HTTP_404_NOT_FOUND
        )

    @staticmethod
    def unauthorized(message='Authentication required'):
        """
        Return a 401 unauthorized response
        
        Args:
            message: Error message
        
        Returns:
            Response object
        """
        return APIResponse.error(
            message=message,
            status=http_status.HTTP_401_UNAUTHORIZED
        )

    @staticmethod
    def server_error(message='Internal server error', context=None):
        """
        Return a 500 server error response
        
        Args:
            message: Error message
            context: Optional context for debugging
        
        Returns:
            Response object
        """
        return APIResponse.error(
            message=message,
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            context=context
        )


def validate_required_fields(data, required_fields):
    """
    Validate that all required fields are present and non-empty
    
    Args:
        data: Dictionary of data to validate (typically request.data)
        required_fields: Set or list of required field names
    
    Returns:
        Dictionary of errors in format { 'field': 'error message' }
    """
    errors = {}
    
    for field in required_fields:
        value = data.get(field)
        
        if value is None:
            errors[field] = f'{field} is required'
        elif isinstance(value, str) and not value.strip():
            errors[field] = f'{field} cannot be empty'
    
    return errors


def validate_field_type(data, field, expected_type, field_name=None):
    """
    Validate a single field's type
    
    Args:
        data: Dictionary of data
        field: Field name
        expected_type: Expected type (int, str, float, etc.)
        field_name: Human-readable field name (defaults to field)
    
    Returns:
        Error message or None if valid
    """
    if not field_name:
        field_name = field
    
    value = data.get(field)
    
    if value is None:
        return None
    
    try:
        expected_type(value)
        return None
    except (ValueError, TypeError):
        return f'{field_name} must be a valid {expected_type.__name__}'


def validate_numeric_range(data, field, min_val=None, max_val=None, field_name=None):
    """
    Validate that a numeric field is within range
    
    Args:
        data: Dictionary of data
        field: Field name
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        field_name: Human-readable field name
    
    Returns:
        Error message or None if valid
    """
    if not field_name:
        field_name = field
    
    value = data.get(field)
    
    if value is None:
        return None
    
    try:
        num_value = int(value) if isinstance(value, str) else value
        
        if min_val is not None and num_value < min_val:
            return f'{field_name} must be at least {min_val}'
        
        if max_val is not None and num_value > max_val:
            return f'{field_name} must not exceed {max_val}'
        
        return None
    except (ValueError, TypeError):
        return f'{field_name} must be a valid number'


def build_validation_errors(data, validators):
    """
    Build validation errors using multiple validators
    
    Args:
        data: Dictionary of data to validate
        validators: List of tuples (field_name, validator_func, error_msg)
    
    Returns:
        Dictionary of errors
    
    Example:
        validators = [
            ('email', lambda x: '@' in x, 'Invalid email format'),
            ('age', lambda x: int(x) >= 18, 'Must be 18 or older'),
        ]
        errors = build_validation_errors(request.data, validators)
    """
    errors = {}
    
    for field, validator_func, error_msg in validators:
        value = data.get(field)
        
        if value is not None:
            try:
                if not validator_func(value):
                    errors[field] = error_msg
            except Exception as e:
                errors[field] = f'Validation error: {str(e)}'
    
    return errors
