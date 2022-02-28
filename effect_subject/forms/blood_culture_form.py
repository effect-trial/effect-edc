from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator
from edc_microbiology.form_validators import BloodCultureSimpleFormValidatorMixin

from ..models import BloodCulture


class BloodCultureFormValidator(
    BloodCultureSimpleFormValidatorMixin,
    FormValidator,
):
    def clean(self):
        self.validate_blood_culture()


class BloodCultureForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = BloodCultureFormValidator

    class Meta:
        model = BloodCulture
        fields = "__all__"
