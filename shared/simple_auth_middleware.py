from django.http import JsonResponse
from .jwt_utils import verify_jwt_token

class SimpleAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip auth for public endpoints
        if request.path in ['/api/auth/login/', '/api/auth/register/', '/health/']:
            return self.get_response(request)
        
        # Get token from header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        token = auth_header.split(' ')[1]
        payload = verify_jwt_token(token)
        
        if not payload:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        # Add user info to request
        request.user_id = payload['user_id']
        request.is_admin = payload.get('is_admin', False)
        return self.get_response(request)

