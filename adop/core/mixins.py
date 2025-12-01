from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class RefugioRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # Verifica que el usuario esté activo y sea refugio
        return self.request.user.is_active and getattr(self.request.user, 'is_refugio', False)

    def handle_no_permission(self):
        # Si no tiene permiso, lo mandamos al inicio (o login)
        return redirect('inicio')