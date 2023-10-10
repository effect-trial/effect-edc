from typing import Tuple

from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item import action_fields, action_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from effect_ae.models import DeathReport

from ..admin_site import effect_prn_admin
from ..forms import EndOfStudyForm
from ..models import EndOfStudy, LossToFollowup


@admin.register(EndOfStudy, site=effect_prn_admin)
class EndOfStudyAdmin(
    SiteModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):
    form = EndOfStudyForm

    additional_instructions = format_html(
        "Note: if the participant is <i>deceased</i>, complete form "
        f"`{DeathReport._meta.verbose_name}` before completing this form. "
        "<BR>If the participant is <i>lost to follow up</i>, complete form "
        f"`{LossToFollowup._meta.verbose_name}` before completing this form."
    )

    fieldsets = (
        [
            "Part 1:",
            {
                "fields": (
                    "subject_identifier",
                    "offschedule_datetime",
                )
            },
        ],
        [
            "Part 2: Reason for study termination",
            {
                "fields": (
                    "offschedule_reason",
                    "other_offschedule_reason",
                    "death_date",
                    "ltfu_date",
                    "consent_withdrawal_reason",
                    "late_exclusion_reasons",
                    "transferred_consent",
                    "invalid_enrol_reason",
                )
            },
        ],
        [
            "Part 3: Further details",
            {"fields": ("comment",)},
        ],
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = ("late_exclusion_reasons",)

    list_display = (
        "subject_identifier",
        "dashboard",
        "offschedule_datetime",
        "action_identifier",
    )

    list_filter = ("offschedule_datetime",)

    radio_fields = {
        "offschedule_reason": admin.VERTICAL,
        "transferred_consent": admin.VERTICAL,
    }

    search_fields = ("subject_identifier", "action_identifier")

    def get_readonly_fields(self, request, obj=None) -> Tuple[str, ...]:
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        action_flds = tuple(fld for fld in action_fields if fld != "action_identifier")
        return tuple(set(action_flds + readonly_fields))
