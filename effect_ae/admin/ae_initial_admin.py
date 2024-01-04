from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields import audit_fieldset_tuple
from edc_action_item import action_fieldset_tuple
from edc_adverse_event.modeladmin_mixins import (
    AeInitialModelAdminMixin,
    fieldset_part_four,
    fieldset_part_one,
    fieldset_part_three,
)
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import effect_ae_admin
from ..forms import AeInitialForm
from ..models import AeInitial


@admin.register(AeInitial, site=effect_ae_admin)
class AeInitialAdmin(SiteModelAdminMixin, AeInitialModelAdminMixin, SimpleHistoryAdmin):
    form = AeInitialForm

    email_contact = settings.EMAIL_CONTACTS.get("ae_reports")
    additional_instructions = format_html(
        "Complete the initial AE report and forward to the TMG. "
        'Email to <a href="mailto:{}">{}</a>',
        email_contact,
        email_contact,
    )

    fieldsets = (
        (None, {"fields": ("subject_identifier", "report_datetime")}),
        fieldset_part_one,
        (
            "Part 2: Hospitalization",
            {
                "fields": (
                    "patient_admitted",
                    "date_admitted",
                    "inpatient_status",
                    "date_discharged",
                )
            },
        ),
        (
            "Part 3: Cause and relationship to study",
            {
                "fields": (
                    "flucon_relation",
                    "flucyt_relation",
                    "ae_study_relation_possibility",
                    "ae_cause",
                    "ae_cause_other",
                )
            },
        ),
        (fieldset_part_three[0].replace("Part 3:", "Part 4:"), fieldset_part_three[1]),
        (fieldset_part_four[0].replace("Part 4:", "Part 5:"), fieldset_part_four[1]),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "ae_cause": admin.VERTICAL,
        "ae_classification": admin.VERTICAL,
        "ae_grade": admin.VERTICAL,
        "ae_study_relation_possibility": admin.VERTICAL,
        "flucon_relation": admin.VERTICAL,
        "flucyt_relation": admin.VERTICAL,
        "inpatient_status": admin.VERTICAL,
        "patient_admitted": admin.VERTICAL,
        "sae": admin.VERTICAL,
        "sae_reason": admin.VERTICAL,
        "susar": admin.VERTICAL,
        "susar_reported": admin.VERTICAL,
    }

    def get_list_display(self, request):
        fields = super().get_list_display(request)
        fields = list(fields)
        fields.remove("__str__")
        return tuple(fields)
