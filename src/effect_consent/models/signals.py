from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from edc_consent import site_consents
from edc_randomization.site_randomizers import site_randomizers
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from effect_prn.models import OnSchedule
from effect_screening.models import SubjectScreening
from effect_subject.models import SubjectVisit

from .subject_consent import SubjectConsent
from .subject_consent_update_v2 import SubjectConsentUpdateV2
from .subject_consent_v1 import SubjectConsentV1
from .subject_consent_v2 import SubjectConsentV2


@receiver(
    post_save,
    weak=False,
    sender=SubjectConsentUpdateV2,
    dispatch_uid="subject_consent_update_v2_on_post_save",
)
def subject_consent_update_v2_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        if created:
            cdef_v1 = site_consents.get_consent_definition(version="1")
            cdef_v2 = site_consents.get_consent_definition(version="2")
            objv1 = cdef_v1.model_cls.objects.get(
                subject_identifier=instance.subject_identifier, version="1"
            )
            objv2 = cdef_v2.model_cls()
            for fld in [
                "screening_identifier",
                "first_name",
                "last_name",
                "initials",
                "gender",
                "language",
                "is_able",
                "is_literate",
                "witness_name",
                "dob",
                "is_dob_estimated",
                "identity",
                "identity_type",
                "confirm_identity",
                "is_incarcerated",
                "consent_reviewed",
                "study_questions",
                "assessment_score",
                "consent_signature",
                "consent_copy",
            ]:
                setattr(objv2, fld, getattr(objv1, fld))

            for fld in [
                "user_created",
                "user_modified",
                "he_substudy",
                "sample_storage",
                "sample_export",
                "hcw_data_sharing",
                "site_id",
                "consent_datetime",
            ]:
                setattr(objv2, fld, getattr(instance, fld))
            objv2.save()


@receiver(
    post_save,
    weak=False,
    dispatch_uid="subject_consent_on_post_save",
)
def subject_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Creates an onschedule instance for this consented subject, if
    it does not exist.
    """
    if not raw:
        if sender in [
            SubjectConsent,
            SubjectConsentV1,
            SubjectConsentV2,
        ]:
            if (
                not created
                or OnSchedule.objects.filter(
                    subject_identifier=instance.subject_identifier
                ).exists()
            ):
                _, schedule = site_visit_schedules.get_by_onschedule_model(
                    "effect_prn.onschedule"
                )
                schedule.refresh_schedule(instance.subject_identifier)
            else:
                subject_screening = SubjectScreening.objects.get(
                    screening_identifier=instance.screening_identifier
                )
                subject_screening.subject_identifier = instance.subject_identifier
                subject_screening.consented = True
                subject_screening.save_base(update_fields=["subject_identifier", "consented"])

                # randomize
                site_randomizers.randomize(
                    "default",
                    identifier=instance.subject_identifier,
                    report_datetime=instance.consent_datetime,
                    site=instance.site,
                    user=instance.user_created,
                    gender=instance.gender,
                )

                # put subject on schedule
                _, schedule = site_visit_schedules.get_by_onschedule_model(
                    "effect_prn.onschedule"
                )
                schedule.put_on_schedule(
                    subject_identifier=instance.subject_identifier,
                    onschedule_datetime=instance.consent_datetime,
                )


@receiver(
    post_delete,
    weak=False,
    dispatch_uid="subject_consent_on_post_delete",
)
def subject_consent_on_post_delete(sender, instance, using, **kwargs):
    """Updates/Resets subject screening."""
    if sender in [
        SubjectConsent,
        SubjectConsentV1,
        SubjectConsentV2,
    ]:
        # don't allow if subject visits exist. This should be caught
        # in the ModelAdmin delete view
        if SubjectVisit.objects.filter(
            subject_identifier=instance.subject_identifier
        ).exists():
            raise ValidationError("Unable to delete consent. Visit data exists.")

        _, schedule = site_visit_schedules.get_by_onschedule_model("effect_prn.onschedule")
        schedule.take_off_schedule(instance.subject_identifier, instance.consent_datetime)

        # update subject screening
        subject_screening = SubjectScreening.objects.get(
            screening_identifier=instance.screening_identifier
        )
        subject_screening.consented = False
        subject_screening.subject_identifier = subject_screening.subject_screening_as_pk
        subject_screening.save()
