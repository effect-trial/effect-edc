from typing import Tuple

from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item import action_fields, action_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import effect_prn_admin
from ..forms import HospitalizationForm
from ..models import Hospitalization


@admin.register(Hospitalization, site=effect_prn_admin)
class HospitalizationAdmin(ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin):

    form = HospitalizationForm

    fieldsets = (
        (None, {"fields": ("subject_identifier", "report_datetime")}),
        (
            "Hospital admission",
            {
                "fields": (
                    "have_details",
                    "admitted_date",
                    "admitted_date_estimated",
                )
            },
        ),
        (
            "Hospital discharge",
            {
                "fields": (
                    "discharged",
                    "discharged_date",
                    "discharged_date_estimated",
                )
            },
        ),
        (
            "Lumbar puncture",
            {
                "fields": (
                    "lp_performed",
                    "lp_count",
                    "csf_positive_cm",
                    "csf_positive_cm_date",
                )
            },
        ),
        ("Narrative", {"fields": ("narrative",)}),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    list_display = ("subject_identifier", "action_identifier")

    radio_fields = {
        "admitted_date_estimated": admin.VERTICAL,
        "csf_positive_cm": admin.VERTICAL,
        "discharged": admin.VERTICAL,
        "discharged_date_estimated": admin.VERTICAL,
        "have_details": admin.VERTICAL,
        "lp_performed": admin.VERTICAL,
    }

    search_fields = ("subject_identifier", "action_identifier")

    def get_readonly_fields(self, request, obj=None) -> Tuple[str, ...]:
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        action_flds = tuple(fld for fld in action_fields if fld != "action_identifier")
        return tuple(set(action_flds + readonly_fields))
