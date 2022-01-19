from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import StudyTreatmentForm
from ..models import StudyTreatment
from .modeladmin import CrfModelAdmin


@admin.register(StudyTreatment, site=effect_subject_admin)
class StudyTreatmentAdmin(CrfModelAdmin):

    form = StudyTreatmentForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Study treatment",
            {
                "fields": (
                    "lp_completed",
                    "cm_confirmed",
                    "cm_tx_administered",
                    "cm_tx_given",
                    "cm_tx_given_other",
                    "tb_tx_given",
                    "tb_tx_given_other",
                    "steroids_administered",
                    "which_steroids",
                    "which_steroids_other",
                    "steroids_course_duration",
                    "co_trimoxazole",
                    "antibiotics",
                    "antibiotics_other",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = ["tb_tx_given", "antibiotics"]

    radio_fields = {
        "lp_completed": admin.VERTICAL,
        "cm_confirmed": admin.VERTICAL,
        "cm_tx_administered": admin.VERTICAL,
        "cm_tx_given": admin.VERTICAL,
        "steroids_administered": admin.VERTICAL,
        "which_steroids": admin.VERTICAL,
        "co_trimoxazole": admin.VERTICAL,
    }
