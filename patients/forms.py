from django import forms

from patients.models import Patient


class PatientOnboardingForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ("date_naissance", "telephone", "adresse")
        widgets = {
            "date_naissance": forms.DateInput(attrs={"type": "date"}),
            "telephone": forms.TextInput(attrs={"placeholder": "+41 …"}),
            "adresse": forms.Textarea(attrs={"rows": 3}),
        }


class RdvMotifForm(forms.Form):
    motif = forms.CharField(
        label="Motif de consultation",
        max_length=255,
        widget=forms.Textarea(attrs={"rows": 3}),
    )
