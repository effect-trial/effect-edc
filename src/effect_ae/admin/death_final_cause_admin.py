from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin
from edc_sites.admin.list_filters import SiteListFilter

from ..admin_site import effect_ae_admin
from ..forms import DeathFinalCauseForm
from ..models import DeathFinalCause
from .list_filters import (
    FinalDeathCauseSetListFilter,
    HasTmgOneListFilter,
    HasTmgTwoListFilter,
)


@admin.register(DeathFinalCause, site=effect_ae_admin)
class DeathFinalCauseAdmin(
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = DeathFinalCauseForm
    show_object_tools = True
    change_list_note = "You may only edit documents from the current site."

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_identifier",
                    "report_datetime",
                ),
            },
        ),
        (
            "Final Cause of Death",
            {
                "fields": (
                    "final_cause_of_death",
                    "final_cause_of_death_other",
                    "verified",
                ),
            },
        ),
        (
            "Original Death Report",
            {
                "description": "Copied from the original Death report (read-only).",
                "fields": (
                    "death_report",
                    "death_report_action_identifier",
                    "cause_of_death",
                    "cause_of_death_other",
                ),
            },
        ),
        (
            "Death Report TMG (1)",
            {
                "description": "Copied from the Death Report TMG (1) (read-only).",
                "fields": (
                    "tmg_one",
                    "tmg_one_action_identifier",
                    "tmg_one_agrees",
                    "tmg_one_cause_of_death",
                    "tmg_one_cause_of_death_other",
                ),
            },
        ),
        (
            "Death Report TMG (2)",
            {
                "description": "Copied from the Death Report TMG (2) (read-only).",
                "fields": (
                    "tmg_two",
                    "tmg_two_action_identifier",
                    "tmg_two_agrees",
                    "tmg_two_cause_of_death",
                    "tmg_two_cause_of_death_other",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "final_cause_of_death": admin.VERTICAL,
        "cause_of_death": admin.VERTICAL,
        "tmg_one_cause_of_death": admin.VERTICAL,
        "tmg_two_cause_of_death": admin.VERTICAL,
    }

    list_display = (
        "subject_identifier",
        "dashboard",
        "final",
        "original",
        "tmg_one_display",
        "tmg_one_agrees_display",
        "tmg_two_display",
        "tmg_two_agrees_display",
        "verified",
    )

    list_filter = (
        FinalDeathCauseSetListFilter,
        "verified",
        HasTmgOneListFilter,
        "tmg_one_agrees",
        HasTmgTwoListFilter,
        "tmg_two_agrees",
        SiteListFilter,
    )

    search_fields = (
        "subject_identifier",
        "death_report_action_identifier",
        "tmg_one_action_identifier",
        "tmg_two_action_identifier",
    )

    readonly_fields = (
        "subject_identifier",
        "death_report",
        "death_report_action_identifier",
        "cause_of_death",
        "cause_of_death_other",
        "tmg_one",
        "tmg_one_action_identifier",
        "tmg_one_agrees",
        "tmg_one_cause_of_death",
        "tmg_one_cause_of_death_other",
        "tmg_two",
        "tmg_two_action_identifier",
        "tmg_two_agrees",
        "tmg_two_cause_of_death",
        "tmg_two_cause_of_death_other",
    )

    @admin.display(description="Final")
    def final(self, obj=None):
        return obj.final_cause_of_death

    @admin.display(description="Death report")
    def original(self, obj=None):
        return obj.cause_of_death

    @admin.display(description="TMG1")
    def tmg_one_display(self, obj=None):
        return obj.tmg_one_cause_of_death

    @admin.display(description="TMG2")
    def tmg_two_display(self, obj=None):
        return obj.tmg_two_cause_of_death

    @admin.display(description="TMG1 Agrees")
    def tmg_one_agrees_display(self, obj=None):
        return obj.tmg_one_agrees

    @admin.display(description="TMG2 Agrees")
    def tmg_two_agrees_display(self, obj=None):
        return obj.tmg_two_agrees

    def get_view_only_site_ids_for_user(self, request) -> list[int]:
        return [s.id for s in request.user.userprofile.sites.all() if s.id != request.site.id]

    def user_may_view_other_sites(self, request) -> bool:  # noqa: ARG002
        return True
