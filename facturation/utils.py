from __future__ import annotations

from django.utils import timezone

from facturation.models import Facture


def next_facture_numero() -> str:
    year = timezone.now().year
    prefix = f"FAC-{year}-"
    last = (
        Facture.objects.filter(numero__startswith=prefix).order_by("-numero").first()
    )
    if last is None:
        return f"{prefix}0001"
    try:
        tail = int(last.numero.replace(prefix, ""))
    except ValueError:
        tail = 0
    return f"{prefix}{tail + 1:04d}"
