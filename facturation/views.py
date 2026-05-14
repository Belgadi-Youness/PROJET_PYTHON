from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView

from clinic_common.mixins import RoleRequiredMixin
from facturation.forms import LigneFactureAjoutForm, PaiementForm
from facturation.models import Facture, LigneFacture, Paiement


def _nav_caissier(active: str) -> list[dict]:
    return [
        {
            "label": "Vue d'ensemble",
            "url_name": "facturation:caissier_dashboard",
            "fragment": None,
            "active": active == "Vue d'ensemble",
        },
    ]


def _shell(request, intro: str) -> dict:
    from types import SimpleNamespace

    u = request.user
    return {
        "clinic": SimpleNamespace(name="AESCULIA"),
        "user_display": (u.get_full_name() or "").strip() or u.email,
        "dashboard_intro": intro,
    }


class CaissierDashboardView(RoleRequiredMixin, ListView):
    required_role = "caissier"
    template_name = "caissier/dashboard.html"
    context_object_name = "factures"

    def get_queryset(self):
        return (
            Facture.objects.filter(
                statut__in=[Facture.Statut.BROUILLON, Facture.Statut.EMISE]
            )
            .select_related("patient__user", "consultation__medecin__user")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "role_key": "caissier",
                "role_title": "Caissier·ère",
                "dashboard_nav": _nav_caissier("Vue d'ensemble"),
            }
        )
        ctx.update(_shell(self.request, "Factures en attente de validation ou de paiement."))
        return ctx


class FactureDetailView(RoleRequiredMixin, TemplateView):
    required_role = "caissier"
    template_name = "caissier/facture_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        facture = get_object_or_404(
            Facture.objects.select_related(
                "patient__user", "consultation__medecin__user"
            ),
            pk=self.kwargs["pk"],
        )
        paye = facture.total_paye_valide()
        reste = facture.total_ttc - paye
        if reste < Decimal("0"):
            reste = Decimal("0")
        ctx.update(
            {
                "role_key": "caissier",
                "role_title": "Caissier·ère",
                "dashboard_nav": _nav_caissier("Vue d'ensemble"),
                "facture": facture,
                "total_paye": paye,
                "reste": reste,
                "ligne_form": LigneFactureAjoutForm(),
                "paiement_form": PaiementForm(),
            }
        )
        ctx.update(_shell(self.request, "Détail facture, lignes et encaissements."))
        return ctx

    def post(self, request, *args, **kwargs):
        facture = get_object_or_404(Facture, pk=self.kwargs["pk"])
        if "valider" in request.POST:
            if facture.statut == Facture.Statut.BROUILLON:
                facture.statut = Facture.Statut.EMISE
                facture.save(update_fields=["statut"])
                messages.success(request, "Facture émise.")
            return redirect(reverse("facturation:facture_detail", kwargs={"pk": facture.pk}))
        if "add_ligne" in request.POST:
            form = LigneFactureAjoutForm(request.POST)
            if form.is_valid():
                ligne = form.save(commit=False)
                ligne.facture = facture
                ligne.save()
                facture.calculer_total()
                messages.success(request, "Ligne ajoutée.")
            else:
                messages.error(request, "Ligne invalide.")
            return redirect(reverse("facturation:facture_detail", kwargs={"pk": facture.pk}))
        if "encaisser" in request.POST:
            form = PaiementForm(request.POST)
            if form.is_valid():
                p = form.save(commit=False)
                p.facture = facture
                p.valide = True
                p.save()
                facture.refresh_from_db()
                if facture.total_paye_valide() >= facture.total_ttc:
                    facture.statut = Facture.Statut.PAYEE
                    facture.save(update_fields=["statut"])
                    messages.success(request, "Paiement enregistré — facture soldée.")
                else:
                    messages.success(request, "Paiement enregistré.")
            else:
                messages.error(request, "Montant ou mode invalide.")
            return redirect(reverse("facturation:facture_detail", kwargs={"pk": facture.pk}))
        return redirect(reverse("facturation:facture_detail", kwargs={"pk": facture.pk}))


class FactureRecuView(RoleRequiredMixin, TemplateView):
    required_role = "caissier"
    template_name = "caissier/recu.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        facture = get_object_or_404(Facture, pk=self.kwargs["pk"])
        ctx.update(
            {
                "role_key": "caissier",
                "role_title": "Caissier·ère",
                "dashboard_nav": _nav_caissier("Vue d'ensemble"),
                "facture": facture,
            }
        )
        ctx.update(_shell(self.request, "Reçu de paiement."))
        return ctx
