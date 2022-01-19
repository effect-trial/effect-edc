from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import NeurologicalForm
from ..models import Neurological
from .fieldsets import reporting_fieldset_tuple
from .modeladmin import CrfModelAdmin


@admin.register(Neurological, site=effect_subject_admin)
class NeurologicalAdmin(CrfModelAdmin):

    form = NeurologicalForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Neurological symptoms",
            {
                "fields": (
                    "meningism",
                    "papilloedema",
                    "focal_neurologic_deficits",
                    "focal_neurologic_deficits_other",
                    "cn_palsy_left_other",
                    "cn_palsy_right_other",
                )
            },
        ),
        reporting_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = ["focal_neurologic_deficits"]

    radio_fields = {
        "meningism": admin.VERTICAL,
        "papilloedema": admin.VERTICAL,
        "reportable_as_ae": admin.VERTICAL,
        "patient_admitted": admin.VERTICAL,
    }
