from rest_framework.permissions import BasePermission
from rest_framework.request import Request

class UserAuthenticated(BasePermission):
    def has_permission(self, request: Request, _):
        restricted_methods = ['POST', 'PATCH', 'DELETE', 'PUT']
        
        if request.method in restricted_methods and (
            request.user.is_anonymous or not request.user.is_admin
        ):
            return False
        
        return True