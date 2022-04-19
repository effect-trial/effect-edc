from django import forms
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NORMAL, OTHER, YES
from edc_constants.utils import get_display
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import ChestXray


class ChestXrayFormValidator(FormValidator):
    def clean(self):

        self.validate_against_sisx_xray_performed()

        self.required_if(YES, field="chest_xray", field_required="chest_xray_date")

        self.m2m_required_if(YES, field="chest_xray", m2m_field="chest_xray_results")

        self.m2m_single_selection_if(NORMAL, m2m_field="chest_xray_results")

        self.m2m_other_specify(
            OTHER,
            m2m_field="chest_xray_results",
            field_other="chest_xray_results_other",
        )

    def validate_against_sisx_xray_performed(self):
        sisx_xray_performed = getattr(
            getattr(self.cleaned_data.get("subject_visit"), "signsandsymptoms", None),
            "xray_performed",
            None,
        )
        if (
            sisx_xray_performed
            and self.cleaned_data.get("chest_xray") != sisx_xray_performed
        ):
            raise forms.ValidationError(
                {
                    "chest_xray": (
                        "Invalid. Previous answer for 'Was an X-ray performed?' "
                        "in 'Signs and Symptoms' "
                        f"was '{get_display(YES_NO_NA, sisx_xray_performed)}'."
                    )
                }
            )


class ChestXrayForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ChestXrayFormValidator

    class Meta:
        model = ChestXray
        fields = "__all__"
