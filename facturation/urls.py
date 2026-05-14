from django.urls import path

from . import views

app_name = "facturation"

urlpatterns = [
    path("dashboard/", views.CaissierDashboardView.as_view(), name="caissier_dashboard"),
    path("facture/<int:pk>/", views.FactureDetailView.as_view(), name="facture_detail"),
    path("facture/<int:pk>/recu/", views.FactureRecuView.as_view(), name="facture_recu"),
]
