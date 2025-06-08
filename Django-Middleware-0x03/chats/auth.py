from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission class that allows authenticated users to perform any action,
    while unauthenticated users can only read (GET) data.
    """
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS: #'GET', 'HEAD', 'OPTIONS':
            return True  # Allow read-only methods for everyone
        return super().has_permission(request, view)  # Check for authenticated users for other methods