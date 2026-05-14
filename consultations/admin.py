from django.contrib import admin

from .models import Consultation, DossierPatient, LigneOrdonnance, Ordonnance


@admin.register(DossierPatient)
class DossierPatientAdmin(admin.ModelAdmin):
    list_display = ("num_dossier", "patient")


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ("patient", "medecin", "date", "termine")
    list_filter = ("termine",)


@admin.register(Ordonnance)
class OrdonnanceAdmin(admin.ModelAdmin):
    list_display = ("consultation", "date", "valide_jusqu")


@admin.register(LigneOrdonnance)
class LigneOrdonnanceAdmin(admin.ModelAdmin):
    list_display = ("ordonnance", "medicament", "dosage")
