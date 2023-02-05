from typing import Any, Optional

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item import action_fieldset_tuple
from edc_action_item.modeladmin_mixins import ActionItemModelAdminMixin
from edc_adverse_event.forms import AeFollowupForm
from edc_adverse_event.modeladmin_mixins import (
    AdverseEventModelAdminMixin,
    NonAeInitialModelAdminMixin,
)
from edc_adverse_event.templatetags.edc_adverse_event_extras import (
    format_ae_followup_description,
    select_description_template,
)
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin


class AeReviewModelAdminMixin(
    ModelAdminSubjectDashboardMixin,
    NonAeInitialModelAdminMixin,
    AdverseEventModelAdminMixin,
    ActionItemModelAdminMixin,
):
    form = AeFollowupForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_identifier",
                    "ae_initial",
                    "report_datetime",
                    "outcome_date",
                    "outcome",
                    "ae_grade",
                    "relevant_history",
                    "followup",
                )
            },
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "outcome": admin.VERTICAL,
        "followup": admin.VERTICAL,
        "ae_grade": admin.VERTICAL,
    }

    list_display = [
        "identifier",
        "dashboard",
        "description",
        "initial_ae",
        "follow_up_reports",
        "user",
    ]

    list_filter = ("ae_grade", "followup", "outcome_date", "report_datetime")

    search_fields = [
        "action_identifier",
        "ae_initial__subject_identifier",
        "ae_initial__action_identifier",
    ]

    @staticmethod
    def description(obj) -> str:
        """Returns a formatted comprehensive description of the SAE
        combining multiple fields.
        """
        context = format_ae_followup_description({}, obj, 80)
        return render_to_string(select_description_template("aefollowup"), context)

    def status(self: Any, obj) -> str:
        follow_up_reports = None
        if obj.followup == YES:
            try:
                ae_followup = self.model.objects.get(parent_action_item=obj.action_item)
            except ObjectDoesNotExist:
                pass
            else:
                follow_up_reports = self.follow_up_reports(ae_followup)
        elif obj.followup == NO and obj.ae_grade != NOT_APPLICABLE:
            follow_up_reports = self.initial_ae(obj)
        if follow_up_reports:
            return format_html(f"{obj.get_outcome_display()}. See {follow_up_reports}.")
        return obj.get_outcome_display()

    def follow_up_reports(self, obj) -> Any:
        return super().follow_up_reports(obj.ae_initial)

    def initial_ae(self: Any, obj) -> Optional[str]:
        """Returns a shortened action identifier."""
        if obj.ae_initial:
            url_name = "_".join(obj.ae_initial._meta.label_lower.split("."))
            namespace = self.admin_site.name
            url = reverse(f"{namespace}:{url_name}_changelist")
            return format_html(
                f'<a data-toggle="tooltip" title="go to ae initial report" '
                f'href="{url}?q={obj.ae_initial.action_identifier}">'
                f"{obj.ae_initial.identifier}</a>"
            )
        return None
