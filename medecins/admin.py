from django.contrib import admin

from .models import Medecin


@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    list_display = ("user", "specialite", "tarif_consultation", "actif")
    list_filter = ("actif", "specialite")
