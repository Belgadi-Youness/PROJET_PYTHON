from django.urls import path

from . import views

app_name = "medecins"

urlpatterns = [
    path("dashboard/", views.MedecinDashboardView.as_view(), name="medecin_dashboard"),
    path(
        "consultation/<int:pk>/",
        views.ConsultationDetailView.as_view(),
        name="consultation_detail",
    ),
]
