from django.db.models.signals import post_save
from django.dispatch import receiver

from patients.models import Patient

from .models import DossierPatient


@receiver(post_save, sender=Patient)
def creer_dossier_patient(sender, instance: Patient, created: bool, **kwargs) -> None:
    if not created:
        return
    DossierPatient.objects.get_or_create(
        patient=instance,
        defaults={"num_dossier": f"D-{instance.num_dossier}"},
    )
