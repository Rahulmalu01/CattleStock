from django.shortcuts import redirect

def moderator_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        allowed_roles = [
            'moderator',
            'manager',
            'admin'
        ]
        if request.user.role in allowed_roles:
            return view_func(request, *args, **kwargs)
        return redirect('home')
    return wrapper