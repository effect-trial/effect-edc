from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import ClinicalNoteForm
from ..models import ClinicalNote
from .modeladmin import CrfModelAdmin


@admin.register(ClinicalNote, site=effect_subject_admin)
class ClinicalNoteAdmin(CrfModelAdmin):
    form = ClinicalNoteForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Clinical note",
            {
                "fields": (
                    "has_comment",
                    "comments",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "has_comment": admin.VERTICAL,
    }
