from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


class Facture(models.Model):
    class Statut(models.TextChoices):
        BROUILLON = "brouillon", _("Brouillon")
        EMISE = "emise", _("Émise")
        PAYEE = "payee", _("Payée")
        ANNULEE = "annulee", _("Annulée")

    consultation = models.OneToOneField(
        "consultations.Consultation",
        on_delete=models.CASCADE,
        related_name="facture",
        verbose_name=_("consultation"),
    )
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="factures",
        verbose_name=_("patient"),
    )
    numero = models.CharField(_("numéro"), max_length=20, unique=True)
    total_ttc = models.DecimalField(
        _("total TTC"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.BROUILLON,
        verbose_name=_("statut"),
    )
    created_at = models.DateTimeField(_("créé le"), auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("facture")
        verbose_name_plural = _("factures")

    def __str__(self) -> str:
        return f"{self.numero} — {self.patient}"

    def calculer_total(self) -> None:
        total = Decimal("0.00")
        for ligne in self.lignes.all():
            total += Decimal(ligne.quantite) * Decimal(str(ligne.prix_unitaire))
        self.total_ttc = total
        self.save(update_fields=["total_ttc"])

    def total_paye_valide(self) -> Decimal:
        s = self.paiements.filter(valide=True).aggregate(s=Sum("montant"))["s"]
        return s or Decimal("0.00")


class LigneFacture(models.Model):
    facture = models.ForeignKey(
        Facture,
        on_delete=models.CASCADE,
        related_name="lignes",
        verbose_name=_("facture"),
    )
    libelle = models.CharField(_("libellé"), max_length=200)
    quantite = models.IntegerField(_("quantité"), default=1)
    prix_unitaire = models.DecimalField(
        _("prix unitaire"),
        max_digits=8,
        decimal_places=2,
    )

    class Meta:
        verbose_name = _("ligne de facture")
        verbose_name_plural = _("lignes de facture")

    def total(self):
        return self.quantite * self.prix_unitaire

    @property
    def montant_ligne(self):
        return self.total()


class Paiement(models.Model):
    class Mode(models.TextChoices):
        ESPECES = "especes", _("Espèces")
        CARTE = "carte", _("Carte bancaire")
        VIREMENT = "virement", _("Virement")
        ASSURANCE = "assurance", _("Assurance")

    facture = models.ForeignKey(
        Facture,
        on_delete=models.CASCADE,
        related_name="paiements",
        verbose_name=_("facture"),
    )
    montant = models.DecimalField(_("montant"), max_digits=10, decimal_places=2)
    mode = models.CharField(
        max_length=20,
        choices=Mode.choices,
        verbose_name=_("mode"),
    )
    date = models.DateTimeField(_("date"), auto_now_add=True)
    valide = models.BooleanField(_("validé"), default=False)

    class Meta:
        ordering = ["-date"]
        verbose_name = _("paiement")
        verbose_name_plural = _("paiements")
