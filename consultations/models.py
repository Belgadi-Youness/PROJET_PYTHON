from django.db import models
from django.utils.translation import gettext_lazy as _


class DossierPatient(models.Model):
    patient = models.OneToOneField(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="dossier",
        verbose_name=_("patient"),
    )
    num_dossier = models.CharField(_("numéro de dossier médical"), max_length=20, unique=True)
    antecedents = models.TextField(_("antécédents"), blank=True)
    allergies = models.TextField(_("allergies"), blank=True)
    created_at = models.DateTimeField(_("créé le"), auto_now_add=True)

    class Meta:
        verbose_name = _("dossier patient")
        verbose_name_plural = _("dossiers patients")

    def __str__(self) -> str:
        return f"Dossier {self.num_dossier}"


class Consultation(models.Model):
    rendez_vous = models.OneToOneField(
        "rendez_vous.RendezVous",
        on_delete=models.CASCADE,
        related_name="consultation",
        verbose_name=_("rendez-vous"),
    )
    medecin = models.ForeignKey(
        "medecins.Medecin",
        on_delete=models.CASCADE,
        related_name="consultations",
        verbose_name=_("médecin"),
    )
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="consultations",
        verbose_name=_("patient"),
    )
    dossier = models.ForeignKey(
        DossierPatient,
        on_delete=models.CASCADE,
        related_name="consultations",
        verbose_name=_("dossier"),
    )
    date = models.DateTimeField(_("date"), auto_now_add=True)
    tension = models.CharField(_("tension"), max_length=20, blank=True)
    poids = models.DecimalField(
        _("poids (kg)"),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    temperature = models.DecimalField(
        _("température (°C)"),
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )
    diagnostic = models.TextField(_("diagnostic"), blank=True)
    compte_rendu = models.TextField(_("compte rendu"), blank=True)
    termine = models.BooleanField(_("terminé"), default=False)

    class Meta:
        ordering = ["-date"]
        verbose_name = _("consultation")
        verbose_name_plural = _("consultations")

    def __str__(self) -> str:
        return f"Consultation {self.patient} — {self.date:%d/%m/%Y %H:%M}"


class Ordonnance(models.Model):
    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE,
        related_name="ordonnance",
        verbose_name=_("consultation"),
    )
    date = models.DateField(_("date"), auto_now_add=True)
    valide_jusqu = models.DateField(_("valide jusqu'au"))

    class Meta:
        verbose_name = _("ordonnance")
        verbose_name_plural = _("ordonnances")

    def __str__(self) -> str:
        return f"Ordonnance du {self.date}"


class LigneOrdonnance(models.Model):
    ordonnance = models.ForeignKey(
        Ordonnance,
        on_delete=models.CASCADE,
        related_name="lignes",
        verbose_name=_("ordonnance"),
    )
    medicament = models.CharField(_("médicament"), max_length=200)
    dosage = models.CharField(_("dosage"), max_length=100)
    duree = models.CharField(_("durée"), max_length=100)
    instructions = models.TextField(_("instructions"), blank=True)

    class Meta:
        verbose_name = _("ligne d'ordonnance")
        verbose_name_plural = _("lignes d'ordonnance")
