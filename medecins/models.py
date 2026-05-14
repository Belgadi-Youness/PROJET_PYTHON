from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Medecin(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medecin_profile",
        verbose_name=_("utilisateur"),
    )
    specialite = models.CharField(_("spécialité"), max_length=100)
    tarif_consultation = models.DecimalField(
        _("tarif consultation"),
        max_digits=8,
        decimal_places=2,
    )
    bio = models.TextField(_("biographie"), blank=True)
    photo = models.ImageField(
        _("photo"),
        upload_to="medecins/",
        blank=True,
        null=True,
    )
    actif = models.BooleanField(_("actif"), default=True)

    class Meta:
        verbose_name = _("médecin")
        verbose_name_plural = _("médecins")

    def __str__(self) -> str:
        return f"Dr. {self.user.get_full_name() or self.user.email} — {self.specialite}"
