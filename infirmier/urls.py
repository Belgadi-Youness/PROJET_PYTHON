from django.urls import path

from . import views

app_name = "infirmier"

urlpatterns = [
    path("dashboard/", views.InfirmierDashboardView.as_view(), name="infirmier_dashboard"),
    path("rdv/<int:pk>/arriver/", views.RdvMarquerArriveView.as_view(), name="rdv_arriver"),
    path("rdv/<int:pk>/constantes/", views.RdvConstantesView.as_view(), name="rdv_constantes"),
]
