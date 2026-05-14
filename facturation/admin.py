from django.contrib import admin

from .models import Facture, LigneFacture, Paiement


class LigneFactureInline(admin.TabularInline):
    model = LigneFacture
    extra = 0


class PaiementInline(admin.TabularInline):
    model = Paiement
    extra = 0


@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ("numero", "patient", "total_ttc", "statut", "created_at")
    list_filter = ("statut",)
    inlines = [LigneFactureInline, PaiementInline]
