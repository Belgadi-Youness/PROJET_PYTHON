from django import forms
from django.forms import inlineformset_factory

from consultations.models import Consultation, LigneOrdonnance, Ordonnance


class ConsultationMedecinForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ("diagnostic", "compte_rendu")
        widgets = {
            "diagnostic": forms.Textarea(attrs={"rows": 4}),
            "compte_rendu": forms.Textarea(attrs={"rows": 5}),
        }


class LigneOrdonnanceForm(forms.ModelForm):
    class Meta:
        model = LigneOrdonnance
        fields = ("medicament", "dosage", "duree", "instructions")
        widgets = {
            "medicament": forms.TextInput(attrs={"placeholder": "Médicament"}),
            "dosage": forms.TextInput(attrs={"placeholder": "Dosage"}),
            "duree": forms.TextInput(attrs={"placeholder": "Durée"}),
            "instructions": forms.Textarea(attrs={"rows": 2, "placeholder": "Instructions"}),
        }


LigneOrdonnanceFormSet = inlineformset_factory(
    Ordonnance,
    LigneOrdonnance,
    form=LigneOrdonnanceForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)
