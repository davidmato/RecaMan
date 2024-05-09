from django.shortcuts import redirect

def check_user_roles(required_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated or not hasattr(request.user, 'rol') \
                    or request.user.rol not in required_roles:
                return redirect('error')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def redirige_segun_rol(required_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            else:
                if request.user.rol == 'CLIENTE':
                    return redirect('areausuario')
                elif request.user.rol == 'ADMIN':
                    return redirect('añadir_mecanico')
        return _wrapped_view
    return decorator
