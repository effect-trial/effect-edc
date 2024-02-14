from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from edc_refusal.models import SubjectRefusal

from .subject_screening import SubjectScreening


@receiver(
    post_save,
    sender=SubjectRefusal,
    weak=False,
    dispatch_uid="update_subjectscreening_refusal_on_post_save",
)
def update_subjectscreening_refusal_on_post_save(
    sender, instance, raw, created, using, **kwargs
):
    if not raw and not kwargs.get("update_fields"):
        try:
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=instance.screening_identifier
            )
        except ObjectDoesNotExist:
            pass
        else:
            subject_screening.refused = True
            subject_screening.save_base(update_fields=["refused"])


@receiver(
    post_delete,
    sender=SubjectRefusal,
    weak=False,
    dispatch_uid="update_subjectscreening_refusal_on_post_delete",
)
def update_subjectscreening_refusal_on_post_delete(sender, instance, using, **kwargs):
    try:
        subject_screening = SubjectScreening.objects.get(
            screening_identifier=instance.screening_identifier
        )
    except ObjectDoesNotExist:
        pass
    else:
        subject_screening.refused = False
        subject_screening.save_base(update_fields=["refused"])
