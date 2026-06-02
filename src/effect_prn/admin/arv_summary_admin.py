from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import effect_prn_admin
from ..models import ArvSummary


@admin.register(ArvSummary, site=effect_prn_admin)
class ArvSummaryAdmin(
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    # form = ArvSummaryForm

    additional_instructions = (
        "This form is not intended for user entry. "
        "There is no validation embedded in this form. "
        "The data in this table imported from Excel"
    )

    autocomplete_fields = (
        "at_screening_regimen",
        "cont_enrol_regimen",
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
                    "at_screening_regimen_other",
                    "at_screening_regimen_start_date_known",
                    "at_screening_regimen_start_date",
                ),
            },
        ),
        (
            "Part 2: ARVs on or after enrolment",
            {
                "fields": (
                    "cont_enrol",
                    "cont_enrol_regimen_changed",
                    "cont_enrol_regimen",
                    "cont_enrol_regimen_other",
                    "cont_enrol_regimen_start_date_known",
                    "cont_enrol_regimen_start_date",
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
        "cont_enrol",
    )

    list_filter = (
        "at_screening",
        "cont_enrol",
    )

    radio_fields = {  # noqa: RUF012
        "at_screening": admin.VERTICAL,
        "at_screening_regimen_start_date_known": admin.VERTICAL,
        "cont_enrol": admin.VERTICAL,
        "cont_enrol_regimen_changed": admin.VERTICAL,
        "cont_enrol_regimen_start_date_known": admin.VERTICAL,
    }

    search_fields = ("subject_identifier",)
