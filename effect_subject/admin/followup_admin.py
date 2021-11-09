from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import FollowupForm
from ..models import Followup
from .modeladmin import CrfModelAdmin


@admin.register(Followup, site=effect_subject_admin)
class FollowupAdmin(CrfModelAdmin):

    form = FollowupForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Followup",
            {
                "fields": (
                    "assessment_type",
                    "info_source",
                    "info_source_other",
                    "survival_status",
                    "hospitalized",
                    "adherence_counselling",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "assessment_type": admin.VERTICAL,
        "info_source": admin.VERTICAL,
        "survival_status": admin.VERTICAL,
        "hospitalized": admin.VERTICAL,
        "adherence_counselling": admin.VERTICAL,
    }
