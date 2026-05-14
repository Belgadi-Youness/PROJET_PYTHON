from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Patient(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile",
        verbose_name=_("utilisateur"),
    )
    num_dossier = models.CharField(_("numéro de dossier"), max_length=20, unique=True)
    date_naissance = models.DateField(_("date de naissance"))
    telephone = models.CharField(_("téléphone"), max_length=20, blank=True)
    adresse = models.TextField(_("adresse"), blank=True)

    class Meta:
        verbose_name = _("patient")
        verbose_name_plural = _("patients")

    def __str__(self) -> str:
        return f"{self.user.get_full_name() or self.user.email} [{self.num_dossier}]"
