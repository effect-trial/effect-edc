from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import effect_prn_admin
from ..forms import ArvSummaryForm
from ..models import ArvSummary


@admin.register(ArvSummary, site=effect_prn_admin)
class ArvSummaryAdmin(
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = ArvSummaryForm

    autocomplete_fields = (
        "at_screening_regimen",
        "cont_enrol_regimen",
        "after_enrol_regimen",
    )

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
            "Part 1: ARVs at screening",
            {
                "fields": (
                    "at_screening",
                    "at_screening_regimen",
                    "at_screening_start_date_known",
                    "at_screening_start_date",
                ),
            },
        ),
        (
            "Part 2: ARVs at enrolment",
            {
                "description": (
                    "This section is applicable if the participant "
                    "was taking ARVs at screening (YES from above)"
                ),
                "fields": (
                    "cont_enrol",
                    "cont_enrol_changed",
                    "cont_enrol_regimen",
                ),
            },
        ),
        (
            "Part 3: ARVs after enrolment",
            {
                "description": (
                    "This section is applicable if (1) the participant "
                    "was NOT taking ARVs at screening (NO from part 1) "
                    "or (2) the participant was taking ARVs at screening "
                    "(YES part 1) but did NOT continue at enrolment (NO from part 2) "
                ),
                "fields": (
                    "after_enrol",
                    "after_enrol_regimen",
                    "after_enrol_start_date_known",
                    "after_enrol_start_date",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "subject_identifier",
        "dashboard",
        "at_screening",
        "cont_enrol",
        "after_enrol",
    )

    list_filter = (
        "at_screening",
        "cont_enrol",
        "after_enrol",
    )

    radio_fields = {  # noqa: RUF012
        "at_screening": admin.VERTICAL,
        "at_screening_start_date_known": admin.VERTICAL,
        "cont_enrol": admin.VERTICAL,
        "cont_enrol_changed": admin.VERTICAL,
        "after_enrol": admin.VERTICAL,
        "after_enrol_start_date_known": admin.VERTICAL,
    }

    search_fields = ("subject_identifier",)
