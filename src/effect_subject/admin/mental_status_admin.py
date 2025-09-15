from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import MentalStatusForm
from ..models import MentalStatus
from .fieldsets import reporting_fieldset_tuple
from .modeladmin import CrfModelAdmin


@admin.register(MentalStatus, site=effect_subject_admin)
class MentalStatusAdmin(CrfModelAdmin):
    form = MentalStatusForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Mental status",
            {
                "fields": (
                    "recent_seizure",
                    "behaviour_change",
                    "confusion",
                    "require_help",
                    "any_other_problems",
                    "modified_rankin_score",
                    "ecog_score",
                    "glasgow_coma_score",
                ),
            },
        ),
        reporting_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "any_other_problems": admin.VERTICAL,
        "behaviour_change": admin.VERTICAL,
        "confusion": admin.VERTICAL,
        "ecog_score": admin.VERTICAL,
        "modified_rankin_score": admin.VERTICAL,
        "patient_admitted": admin.VERTICAL,
        "recent_seizure": admin.VERTICAL,
        "reportable_as_ae": admin.VERTICAL,
        "require_help": admin.VERTICAL,
    }
