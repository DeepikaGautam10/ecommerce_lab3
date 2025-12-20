from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Please login to continue.')
                return redirect('accounts:login')
            
            # Check if user is admin (staff or superuser)
            if 'admin' in allowed_roles:
                if request.user.is_staff or request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
            
            # If you have custom roles, check them here
            # For now, just check is_staff for admin access
            if request.user.is_staff or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, 'You do not have permission to access this page.')
            raise PermissionDenied
        return wrapper
    return decorator

def permission_required(permission_codename):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Please login to continue.')
                return redirect('accounts:login')
            
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check Django's built-in permissions
            if request.user.has_perm(permission_codename):
                return view_func(request, *args, **kwargs)
            
            messages.error(request, 'You do not have permission to perform this action.')
            raise PermissionDenied
        return wrapper
    return decorator