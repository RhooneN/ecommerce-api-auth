from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .services import AuthenticationService
import logging

logger = logging.getLogger(__name__)

class JWTAuthenticationMiddleware(MiddlewareMixin):
    """Middleware to validate JWT tokens"""
    
    # Endpoints that don't require authentication
    EXEMPT_PATHS = [
        '/api/auth/login/',
        '/api/auth/register/',
        '/api/health/',
        '/admin/'
    ]
    
    def process_request(self, request):
        # Skip authentication for exempt paths
        if any(request.path.startswith(path) for path in self.EXEMPT_PATHS):
            return None
        
        # Get token from Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        token = auth_header.split(' ')[1]
        payload = AuthenticationService.validate_token(token)
        
        if not payload:
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)
        
        # Add user info to request
        request.jwt_payload = payload
        request.user_id = payload.get('user_id')
        request.user_permissions = payload.get('permissions', [])
        
        return None

import jwt
from django.conf import settings
from typing import Dict, List, Optional
import requests
import logging

logger = logging.getLogger(__name__)

class JWTValidator:
    """Utility class for JWT validation across services"""
    
    @staticmethod
    def validate_token(token: str) -> Optional[Dict]:
        """Validate JWT token"""
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=['HS256'],
                options={'verify_exp': True}
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
    
    @staticmethod
    def has_permission(user_permissions: List[str], required_permission: str) -> bool:
        """Check if user has required permission"""
        return required_permission in user_permissions or 'admin.full_access' in user_permissions
    
    @staticmethod
    def validate_service_token(token: str, service_name: str) -> bool:
        """Validate token for specific service"""
        payload = JWTValidator.validate_token(token)
        if not payload:
            return False
        
        # Check if token is intended for this service
        audiences = payload.get('aud', [])
        return service_name in audiences or not audiences  # Allow if no specific audience
