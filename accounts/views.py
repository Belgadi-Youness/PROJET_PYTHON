from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import AesculiaLoginForm

ROLE_REDIRECTS = {
    "patient":   reverse_lazy("patients:patient_dashboard"),
    "medecin":   reverse_lazy("medecins:medecin_dashboard"),
    "infirmier": reverse_lazy("infirmier:infirmier_dashboard"),
    "caissier":  reverse_lazy("facturation:caissier_dashboard"),
}


class AesculiaLogoutView(LogoutView):
    """Compatible Django 5 — fonctionne en GET et POST."""
    http_method_names = ["get", "post", "head", "options", "trace"]
    next_page = reverse_lazy("landing")

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.next_page)


class AesculiaLoginView(LoginView):
    """Connexion unique — redirection selon le rôle."""
    template_name = "auth/login.html"
    authentication_form = AesculiaLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember = self.request.POST.get("remember")
        if remember:
            self.request.session.set_expiry(60 * 60 * 24 * 14)
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or (getattr(user, "role", None) == "admin" and user.is_staff):
            return str(reverse_lazy("admin:index"))
        role = getattr(user, "role", None) or "patient"
        url = ROLE_REDIRECTS.get(role)
        return str(url) if url else str(reverse_lazy("patients:patient_dashboard"))