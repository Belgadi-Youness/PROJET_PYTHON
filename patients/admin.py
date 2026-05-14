from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("num_dossier", "user", "date_naissance", "telephone")
    search_fields = ("num_dossier", "user__email", "user__first_name", "user__last_name")
