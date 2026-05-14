from django.db import models
from django.utils.translation import gettext_lazy as _


class RendezVous(models.Model):
    class Statut(models.TextChoices):
        PLANIFIE = "planifie", _("Planifié")
        CONFIRME = "confirme", _("Confirmé")
        ARRIVE = "arrive", _("Arrivé")
        EN_COURS = "en_cours", _("En cours")
        TERMINE = "termine", _("Terminé")
        ANNULE = "annule", _("Annulé")

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="rendez_vous",
        verbose_name=_("patient"),
    )
    medecin = models.ForeignKey(
        "medecins.Medecin",
        on_delete=models.CASCADE,
        related_name="rendez_vous",
        verbose_name=_("médecin"),
    )
    date_heure = models.DateTimeField(_("date et heure"))
    motif = models.CharField(_("motif"), max_length=255)
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.PLANIFIE,
        verbose_name=_("statut"),
    )
    notes = models.TextField(_("notes"), blank=True)
    created_at = models.DateTimeField(_("créé le"), auto_now_add=True)

    class Meta:
        ordering = ["date_heure"]
        verbose_name = _("rendez-vous")
        verbose_name_plural = _("rendez-vous")

    def __str__(self) -> str:
        return f"RDV {self.patient} → {self.medecin} le {self.date_heure:%d/%m %H:%M}"
