from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_constants.constants import OTHER, YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..constants import HEADACHE, VISUAL_LOSS
from ..models import SignsAndSymptoms


class SignsAndSymptomsFormValidator(FormValidator):
    def clean(self) -> None:
        # TODO: Validate that patient can't specify UNKNOWN for
        #  any_sx (e.g. if an in-person or telephone/patient visit)

        self.validate_current_sx()
        self.validate_reportable_gte_g3()

        self.m2m_other_specify(
            HEADACHE, m2m_field="current_sx", field_other="headache_duration"
        )
        self.m2m_other_specify(
            VISUAL_LOSS, m2m_field="current_sx", field_other="visual_field_loss"
        )
        self.applicable_if(YES, field="any_sx", field_applicable="patient_admitted")

        self.validate_cm_sx()

    def validate_current_sx(self):
        self.m2m_required_if(
            response=YES,
            field="any_sx",
            m2m_field="current_sx",
        )
        self.m2m_other_specify(
            OTHER, m2m_field="current_sx", field_other="current_sx_other"
        )

    def validate_reportable_gte_g3(self):
        self.applicable_if(YES, field="any_sx", field_applicable="reportable_as_ae")
        self.m2m_required_if(
            response=YES,
            field="reportable_as_ae",
            m2m_field="current_sx_gte_g3",
        )
        self.m2m_other_specify(
            OTHER, m2m_field="current_sx_gte_g3", field_other="current_sx_gte_g3_other"
        )
        sx_gte_g3_selections = self.get_m2m_selected("current_sx_gte_g3")
        if sx_gte_g3_selections:
            sx_selections = self.get_m2m_selected("current_sx")
            if [x for x in sx_gte_g3_selections if x not in sx_selections]:
                raise forms.ValidationError(
                    {
                        "current_sx_gte_g3": (
                            "Invalid selection. Must be from above list of signs and symptoms"
                        )
                    }
                )

    def validate_cm_sx(self):
        self.applicable_if(YES, field="any_sx", field_applicable="cm_sx")
        # TODO: Test "cm_sx_..." behaviour as expected
        self.applicable_if(YES, field="cm_sx", field_applicable="cm_sx_lp_done")
        self.applicable_if(YES, field="cm_sx", field_applicable="cm_sx_bloods_taken")
        self.applicable_if(
            YES, field="cm_sx", field_applicable="cm_sx_patient_admitted"
        )


class SignsAndSymptomsForm(CrfModelFormMixin, ActionItemFormMixin, forms.ModelForm):
    form_validator_cls = SignsAndSymptomsFormValidator

    class Meta:
        model = SignsAndSymptoms
        fields = "__all__"
