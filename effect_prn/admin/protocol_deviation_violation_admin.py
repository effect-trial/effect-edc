from typing import Tuple

from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item import action_fields, action_fieldset_tuple
from edc_constants.constants import CLOSED, OPEN
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import effect_prn_admin
from ..forms import ProtocolDeviationViolationForm
from ..models import ProtocolDeviationViolation


@admin.register(ProtocolDeviationViolation, site=effect_prn_admin)
class ProtocolDeviationViolationAdmin(ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin):

    form = ProtocolDeviationViolationForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_identifier",
                    "report_datetime",
                    "short_description",
                    "report_type",
                )
            },
        ),
        (
            "Details of protocol violation",
            {
                "description": (
                    "The following questions are only required if "
                    "this is a protocol violation."
                ),
                "fields": (
                    "safety_impact",
                    "safety_impact_details",
                    "study_outcomes_impact",
                    "study_outcomes_impact_details",
                    "violation_datetime",
                    "violation_type",
                    "violation_type_other",
                    "violation_description",
                    "violation_reason",
                ),
            },
        ),
        (
            "Actions taken",
            {
                "description": (
                    "The following questions are required before the report is closed."
                ),
                "fields": (
                    "corrective_action_datetime",
                    "corrective_action",
                    "preventative_action_datetime",
                    "preventative_action",
                    "action_required",
                ),
            },
        ),
        ("Report status", {"fields": ("report_status", "report_closed_datetime")}),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "action_required": admin.VERTICAL,
        "report_status": admin.VERTICAL,
        "report_type": admin.VERTICAL,
        "safety_impact": admin.VERTICAL,
        "study_outcomes_impact": admin.VERTICAL,
        "violation_type": admin.VERTICAL,
    }

    list_display = (
        "subject_identifier",
        "dashboard",
        "description",
        "report_datetime",
        "status",
        "action_required",
        "report_type",
        "action_identifier",
        "user_created",
    )

    list_filter = ("action_required", "report_status", "report_type")

    search_fields = [
        "subject_identifier",
        "action_identifier",
        "short_description",
    ]

    def get_readonly_fields(self, request, obj=None) -> Tuple[str, ...]:
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        action_flds = tuple(fld for fld in action_fields if fld != "action_identifier")
        return tuple(set(action_flds + readonly_fields))

    def status(self, obj=None):
        if obj.report_status == CLOSED:
            return format_html(f'<font color="green">{obj.report_status.title()}</font>')
        elif obj.report_status == OPEN:
            return format_html(f'<font color="red">{obj.report_status.title()}</font>')
        return obj.report_status.title()

    def description(self, obj=None):
        return obj.short_description.title()
