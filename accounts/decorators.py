from django.shortcuts import redirect

def allowed_roles(roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            return redirect('home')
        return wrapper
    return decorator