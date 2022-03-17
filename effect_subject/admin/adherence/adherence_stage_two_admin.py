from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ...admin_site import effect_subject_admin
from ...forms import AdherenceStageTwoForm
from ...models import AdherenceStageTwo
from ..modeladmin import CrfModelAdmin


@admin.register(AdherenceStageTwo, site=effect_subject_admin)
class AdherenceStageTwoAdmin(CrfModelAdmin):

    form = AdherenceStageTwoForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Adherence counselling",
            {
                "fields": (
                    "adherence_counselling",
                    "adherence_counselling_reason_no",
                    "diary_issued",
                    "diary_issued_reason_no",
                )
            },
        ),
        ("Adherence summary", {"fields": ("adherence_narrative",)}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "adherence_counselling": admin.VERTICAL,
        "diary_issued": admin.VERTICAL,
    }
