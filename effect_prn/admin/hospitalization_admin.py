from copy import copy

from django.contrib import admin
from edc_action_item import action_fields, action_fieldset_tuple
from edc_model_admin import SimpleHistoryAdmin, audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

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

    list_display = ("subject_identifier", "tracking_identifier", "action_identifier")

    radio_fields = {
        "admitted_date_estimated": admin.VERTICAL,
        "csf_positive_cm": admin.VERTICAL,
        "discharged": admin.VERTICAL,
        "discharged_date_estimated": admin.VERTICAL,
        "have_details": admin.VERTICAL,
        "lp_performed": admin.VERTICAL,
    }

    search_fields = ("subject_identifier", "action_identifier", "tracking_identifier")

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        action_flds = copy(list(action_fields))
        fields = list(action_flds) + list(fields)
        return fields
