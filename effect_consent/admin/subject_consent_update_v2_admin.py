from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_action_item import action_fields, action_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import effect_consent_admin
from ..forms import SubjectConsentUpdateV2Form
from ..models import SubjectConsentUpdateV2


@admin.register(SubjectConsentUpdateV2, site=effect_consent_admin)
class SubjectConsentUpdateV2Admin(
    SiteModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):
    form = SubjectConsentUpdateV2Form

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

    search_fields = ("subject_identifier", "action_identifier")

    radio_fields = {
        "he_substudy": admin.VERTICAL,
        "sample_storage": admin.VERTICAL,
        "sample_export": admin.VERTICAL,
        "hcw_data_sharing": admin.VERTICAL,
    }

    def get_readonly_fields(self, request, obj=None) -> tuple[str, ...]:
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        action_flds = tuple(fld for fld in action_fields if fld != "action_identifier")
        return tuple(set(action_flds + readonly_fields))
