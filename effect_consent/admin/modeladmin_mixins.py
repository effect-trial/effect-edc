from django.contrib import admin
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django_audit_fields import audit_fieldset_tuple
from edc_identifier import SubjectIdentifierError, is_subject_identifier_or_raise

from effect_consent.models import SubjectConsent
from effect_screening.models import SubjectScreening
from effect_subject.models import SubjectVisit


class EffectSubjectConsentAdminMixin:
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "screening_identifier",
                    "subject_identifier",
                    "first_name",
                    "last_name",
                    "initials",
                    "gender",
                    "language",
                    "is_able",
                    "is_literate",
                    "witness_name",
                    "consent_datetime",
                    "dob",
                    "is_dob_estimated",
                    "identity",
                    "identity_type",
                    "confirm_identity",
                    "is_incarcerated",
                )
            },
        ),
        (
            "Substudy, Specimens and Data Sharing",
            {
                "fields": (
                    "he_substudy",
                    "sample_storage",
                    "sample_export",
                    "hcw_data_sharing",
                ),
            },
        ),
        (
            "Review Questions",
            {
                "fields": (
                    "consent_reviewed",
                    "study_questions",
                    "assessment_score",
                    "consent_signature",
                    "consent_copy",
                ),
                "description": "The following questions are directed to the interviewer.",
            },
        ),
        audit_fieldset_tuple,
    )

    search_fields = ("subject_identifier", "screening_identifier", "identity")

    radio_fields = {
        "gender": admin.VERTICAL,
        "assessment_score": admin.VERTICAL,
        "consent_copy": admin.VERTICAL,
        "consent_reviewed": admin.VERTICAL,
        "consent_signature": admin.VERTICAL,
        "is_dob_estimated": admin.VERTICAL,
        "identity_type": admin.VERTICAL,
        "is_incarcerated": admin.VERTICAL,
        "is_able": admin.VERTICAL,
        "is_literate": admin.VERTICAL,
        "language": admin.VERTICAL,
        "study_questions": admin.VERTICAL,
        "he_substudy": admin.VERTICAL,
        "sample_storage": admin.VERTICAL,
        "sample_export": admin.VERTICAL,
        "hcw_data_sharing": admin.VERTICAL,
    }

    readonly_fields = [
        "he_substudy",
        "sample_storage",
        "sample_export",
        "hcw_data_sharing",
    ]

    def delete_view(self, request, object_id, extra_context=None):
        """Prevent deletion if SubjectVisit objects exist."""
        extra_context = extra_context or {}
        obj = SubjectConsent.objects.get(id=object_id)
        try:
            protected = [SubjectVisit.objects.get(subject_identifier=obj.subject_identifier)]
        except ObjectDoesNotExist:
            protected = None
        except MultipleObjectsReturned:
            protected = SubjectVisit.objects.filter(subject_identifier=obj.subject_identifier)
        extra_context.update({"protected": protected})
        return super().delete_view(request, object_id, extra_context)

    def get_next_options(self, request=None, **kwargs):
        """Returns the key/value pairs from the "next" querystring
        as a dictionary.
        """
        next_options = super().get_next_options(request=request, **kwargs)
        try:
            is_subject_identifier_or_raise(next_options["subject_identifier"])
        except SubjectIdentifierError:
            next_options["subject_identifier"] = SubjectScreening.objects.get(
                subject_identifier_as_pk=next_options["subject_identifier"]
            ).subject_identifier
        except KeyError:
            pass
        return next_options
