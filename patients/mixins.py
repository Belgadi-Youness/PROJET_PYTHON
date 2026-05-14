"""Mixins espace patient."""

from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse

from patients.models import Patient


class PatientAccountMixin(LoginRequiredMixin):
    """Patient connecté avec profil Patient obligatoire."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if getattr(request.user, "role", None) != "patient":
            return redirect(reverse("landing"))
        try:
            request.patient_profile = request.user.patient_profile  # type: ignore[attr-defined]
        except Patient.DoesNotExist:
            return redirect(reverse("patients:onboarding"))
        return super().dispatch(request, *args, **kwargs)
