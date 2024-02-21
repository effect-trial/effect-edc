from typing import Tuple

from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item import action_fields, action_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import effect_prn_admin
from ..forms import HospitalizationForm
from ..models import Hospitalization
from .list_filters import AdmittedDateListFilter, DischargedDateListFilter


@admin.register(Hospitalization, site=effect_prn_admin)
class HospitalizationAdmin(
    SiteModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):
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

    list_display = (
        "subject_identifier",
        "dashboard",
        "admitted_dte",
        "is_discharged",
        "discharged_dte",
        "lp",
    )

    list_filter = (
        AdmittedDateListFilter,
        DischargedDateListFilter,
        "discharged",
        "lp_performed",
    )

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

    @admin.display(description="Admitted Date", ordering="admitted_date")
    def admitted_dte(self, obj):
        return obj.admitted_date

    @admin.display(description="discharged", ordering="discharged")
    def is_discharged(self, obj):
        return obj.discharged

    @admin.display(description="Discharged Date", ordering="discharged_date")
    def discharged_dte(self, obj):
        return obj.discharged_date

    @admin.display(description="LP", ordering="lp_performed")
    def lp(self, obj):
        return obj.lp_performed
