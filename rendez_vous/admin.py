from django.contrib import admin

from .models import RendezVous


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ("patient", "medecin", "date_heure", "statut", "motif")
    list_filter = ("statut",)
    search_fields = ("motif", "patient__num_dossier")
