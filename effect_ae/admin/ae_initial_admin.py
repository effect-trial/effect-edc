from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django_audit_fields import audit_fieldset_tuple
from edc_action_item import action_fieldset_tuple
from edc_adverse_event.forms import AeInitialForm
from edc_adverse_event.modeladmin_mixins import (
    AeInitialModelAdminMixin,
    fieldset_part_one,
)
from edc_adverse_event.modeladmin_mixins.ae_initial import (
    fieldset_part_four,
    fieldset_part_three,
)
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import effect_ae_admin
from ..form_validators.ae_initial import AeInitialFormValidator
from ..models import AeInitial


class CustomAeInitialForm(AeInitialForm):

    form_validator = AeInitialFormValidator


@admin.register(AeInitial, site=effect_ae_admin)
class AeInitialAdmin(AeInitialModelAdminMixin, SimpleHistoryAdmin):

    form = CustomAeInitialForm
    email_contact = settings.EMAIL_CONTACTS.get("ae_reports")
    additional_instructions = mark_safe(
        "Complete the initial AE report and forward to the TMG. "
        f'Email to <a href="mailto:{email_contact}">{email_contact}</a>'
    )

    fieldsets = (
        (None, {"fields": ("subject_identifier", "report_datetime")}),
        fieldset_part_one,
        (
            "Hospitalization",
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
            "Part 2: Cause and relationship to study",
            {
                "fields": (
                    "ae_study_relation_possibility",
                    "fluconazole_relation",
                    "flucytosine_relation",
                    "ae_cause",
                    "ae_cause_other",
                )
            },
        ),
        fieldset_part_three,
        fieldset_part_four,
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "ae_cause": admin.VERTICAL,
        "ae_classification": admin.VERTICAL,
        "ae_grade": admin.VERTICAL,
        "ae_study_relation_possibility": admin.VERTICAL,
        "fluconazole_relation": admin.VERTICAL,
        "flucytosine_relation": admin.VERTICAL,
        "inpatient_status": admin.VERTICAL,
        "patient_admitted": admin.VERTICAL,
        "sae": admin.VERTICAL,
        "sae_reason": admin.VERTICAL,
        "susar": admin.VERTICAL,
        "susar_reported": admin.VERTICAL,
    }
