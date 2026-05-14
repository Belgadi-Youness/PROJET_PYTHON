from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Iterator

from django.utils import timezone

from medecins.models import Medecin
from rendez_vous.models import RendezVous

# Statuts qui bloquent un créneau déjà pris
_STATUTS_OCCUPATION = (
    RendezVous.Statut.PLANIFIE,
    RendezVous.Statut.CONFIRME,
    RendezVous.Statut.ARRIVE,
    RendezVous.Statut.EN_COURS,
)


def creneaux_libres(medecin: Medecin, jour: date) -> Iterator[datetime]:
    """Itère les débuts de créneaux (30 min) entre 08:00 et 17:30, fuseau Django."""
    debut_jour = timezone.make_aware(datetime.combine(jour, time(8, 0)))
    fin_jour = timezone.make_aware(datetime.combine(jour, time(17, 30)))
    pris = set(
        RendezVous.objects.filter(
            medecin=medecin,
            date_heure__date=jour,
            statut__in=_STATUTS_OCCUPATION,
        ).values_list("date_heure", flat=True)
    )
    cur = debut_jour
    step = timedelta(minutes=30)
    while cur <= fin_jour:
        if cur not in pris:
            yield cur
        cur += step


def prochains_jours(n: int = 14) -> list[date]:
    today = timezone.localdate()
    return [today + timedelta(days=i) for i in range(n)]
