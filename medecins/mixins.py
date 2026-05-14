from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse

from medecins.models import Medecin


class MedecinAccountMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if getattr(request.user, "role", None) != "medecin":
            return redirect(reverse("landing"))
        try:
            request.medecin_profile = request.user.medecin_profile  # type: ignore[attr-defined]
        except Medecin.DoesNotExist:
            return redirect(reverse("landing"))
        return super().dispatch(request, *args, **kwargs)
