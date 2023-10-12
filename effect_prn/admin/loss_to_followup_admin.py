from typing import Tuple

from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item import action_fields, action_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import effect_prn_admin
from ..forms import LossToFollowupForm
from ..models import LossToFollowup


@admin.register(LossToFollowup, site=effect_prn_admin)
class LossToFollowupAdmin(
    SiteModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):
    form = LossToFollowupForm

    fieldsets = (
        (None, {"fields": ("subject_identifier", "report_datetime")}),
        (
            "Loss to followup",
            {
                "fields": (
                    "last_seen_datetime",
                    "number_consecutive_missed_visits",
                    "last_missed_visit_datetime",
                    "home_visited",
                    "home_visit_detail",
                    "loss_category",
                    "loss_category_other",
                    "comment",
                )
            },
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    list_display = (
        "subject_identifier",
        "dashboard",
        "last_seen_datetime",
        "number_consecutive_missed_visits",
        "home_visited",
    )

    list_filter = (
        "last_seen_datetime",
        "last_missed_visit_datetime",
        "number_consecutive_missed_visits",
    )

    radio_fields = {
        "home_visited": admin.VERTICAL,
        "loss_category": admin.VERTICAL,
    }

    search_fields = ("subject_identifier", "action_identifier")

    def get_readonly_fields(self, request, obj=None) -> Tuple[str, ...]:
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        action_flds = tuple(fld for fld in action_fields if fld != "action_identifier")
        return tuple(set(action_flds + readonly_fields))
