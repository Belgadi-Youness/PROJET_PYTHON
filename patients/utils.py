from __future__ import annotations

import secrets

from django.utils import timezone


def generer_num_dossier() -> str:
    return f"P-{timezone.now().strftime('%Y%m')}-{secrets.token_hex(2).upper()}"
