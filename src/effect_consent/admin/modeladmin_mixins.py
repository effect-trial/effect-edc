from django.contrib import admin, messages
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django_audit_fields import audit_fieldset_tuple
from edc_auth.constants import PII, PII_VIEW
from edc_identifier import SubjectIdentifierError, is_subject_identifier_or_raise
from rangefilter.filters import DateRangeFilterBuilder

from effect_consent.models import SubjectConsent
from effect_screening.models import SubjectScreening
from effect_subject.models import SubjectVisit


def remove_fields_for_blinded_users(request: WSGIRequest, fields: tuple) -> tuple:
    """You need to secure custom SimpleListFilters yourself"""
    if not request.user.groups.filter(name__in=[PII, PII_VIEW]).exists():
        fields = list(fields)
        for f in fields:
            if isinstance(f, str):
                if (
                    "assignment" in f
                    or "first_name" in f
                    or "last_name" in f
                    or "initials" in f
                    or "identity" in f
                    or "confirm_identity" in f
                ):
                    fields.remove(f)
            elif isinstance(f, tuple):
                f, _ = f  # noqa: PLW2901
                if (
                    "assignment" in f
                    or "first_name" in f
                    or "last_name" in f
                    or "initials" in f
                    or "identity" in f
                    or "confirm_identity" in f
                ):
                    fields.remove(f)
        fields = tuple(fields)
    return fields


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
                ),
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

    list_filters = (("consent_datetime", DateRangeFilterBuilder()),)

    search_fields = ("subject_identifier", "screening_identifier", "identity")

    radio_fields = {  # noqa: RUF012
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

    readonly_fields = (
        "he_substudy",
        "sample_storage",
        "sample_export",
        "hcw_data_sharing",
    )

    def save_model(self, request, obj, form, change):
        if not request.user.groups.filter(name__in=[PII, PII_VIEW]).exists():
            messages.error(
                request,
                "Form not saved. User account does not have PII or PII_VIEW permissions.",
            )
        else:
            super().save_model(request, obj, form, change)

    def get_list_display(self, request):
        fields = super().get_list_display(request)
        return remove_fields_for_blinded_users(request, fields)

    def get_list_filter(self, request):
        fields = super().get_list_filter(request)
        return remove_fields_for_blinded_users(request, fields)

    def get_search_fields(self, request):
        fields = super().get_search_fields(request)
        return remove_fields_for_blinded_users(request, fields)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.groups.filter(name__in=[PII, PII_VIEW]).exists():
            pii_fields = [
                "first_name",
                "last_name",
                "initials",
                "identity",
                "confirm_identity",
            ]
            new_fieldsets = []
            for fieldset in fieldsets:
                fieldset[1]["fields"] = [
                    f for f in fieldset[1]["fields"] if f not in pii_fields
                ]
                new_fieldsets.append(fieldset)
            return new_fieldsets
        return fieldsets

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
                subject_identifier_as_pk=next_options["subject_identifier"],
            ).subject_identifier
        except KeyError:
            pass
        return next_options
