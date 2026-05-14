from django import forms

from facturation.models import LigneFacture, Paiement


class LigneFactureAjoutForm(forms.ModelForm):
    class Meta:
        model = LigneFacture
        fields = ("libelle", "quantite", "prix_unitaire")
        widgets = {
            "libelle": forms.TextInput(attrs={"placeholder": "Libellé"}),
            "quantite": forms.NumberInput(attrs={"min": 1, "step": 1}),
            "prix_unitaire": forms.NumberInput(attrs={"step": "0.01"}),
        }


class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ("montant", "mode")
        widgets = {
            "montant": forms.NumberInput(attrs={"step": "0.01"}),
        }
