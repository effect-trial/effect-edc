from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_action_item.fieldsets import action_fields, action_fieldset_tuple
from edc_constants.constants import YES
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import effect_consent_admin
from ..forms import SubjectConsentUpdateV2Form
from ..models import SubjectConsentUpdateV2
from .list_filters import ConsentDateListFilter


@admin.register(SubjectConsentUpdateV2, site=effect_consent_admin)
class SubjectConsentUpdateV2Admin(
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = SubjectConsentUpdateV2Form
    show_dashboard_in_list_display_pos = 1

    fieldsets = (
        (
            None,
            {"fields": ("subject_identifier", "consent_datetime")},
        ),
        (
            "Substudy, Specimens and Data Sharing",
            {
                "fields": (
                    "he_substudy",
                    "sample_storage",
                    "sample_export",
                    "hcw_data_sharing",
                ),
            },
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    list_display = (
        "subject_identifier",
        "consent_datetime",
        "consent_he_substudy",
        "consent_sample_storage",
        "consent_sample_export",
        "consent_hcw_data_sharing",
    )

    list_filter = (
        ConsentDateListFilter,
        "he_substudy",
        "sample_storage",
        "sample_export",
        "hcw_data_sharing",
    )

    search_fields = ("subject_identifier", "action_identifier")

    radio_fields = {  # noqa: RUF012
        "he_substudy": admin.VERTICAL,
        "sample_storage": admin.VERTICAL,
        "sample_export": admin.VERTICAL,
        "hcw_data_sharing": admin.VERTICAL,
    }

    @admin.display(description="HE sub-study", ordering="he_substudy")
    def consent_he_substudy(self, obj=None) -> bool:
        return obj.he_substudy == YES

    consent_he_substudy.boolean = True

    @admin.display(description="Sample storage", ordering="sample_storage")
    def consent_sample_storage(self, obj=None) -> bool:
        return obj.sample_storage == YES

    consent_sample_storage.boolean = True

    @admin.display(description="Sample export", ordering="sample_export")
    def consent_sample_export(self, obj=None) -> bool:
        return obj.sample_export == YES

    consent_sample_export.boolean = True

    @admin.display(description="HCW data sharing", ordering="hcw_data_sharing")
    def consent_hcw_data_sharing(self, obj=None) -> bool:
        return obj.hcw_data_sharing == YES

    consent_hcw_data_sharing.boolean = True

    def get_readonly_fields(self, request, obj=None) -> tuple[str, ...]:
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        action_flds = tuple(fld for fld in action_fields if fld != "action_identifier")
        return tuple(set(action_flds + readonly_fields))
