from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            profile = getattr(request.user, 'profile', None)
            role = profile.role if profile else None
            if role in allowed_roles:
                return view_func(request, *args, **kwargs)
            # allow superuser to access admin pages
            if request.user.is_superuser and 'admin' in allowed_roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator
