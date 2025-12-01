from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def refugio_required(view_func):
    def check_refugio(user):

        return user.is_active and user.is_authenticated and getattr(user, 'is_refugio', False)
    decorated_view_func = user_passes_test(check_refugio, login_url='inicio')
    return decorated_view_func(view_func)