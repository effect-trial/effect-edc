from django import forms
from edc_action_item.forms.action_item_form_mixin import ActionItemFormMixin
from edc_constants.constants import YES
from edc_form_validators.form_validator import FormValidator
from edc_form_validators.form_validator_mixins import FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_sites.forms import SiteModelFormMixin

from ..models import LossToFollowup


class LossToFollowupFormValidator(FormValidator):
    def clean(self):
        self.required_if(YES, field="home_visit", field_required="home_visit_detail")
        self.validate_other_specify(
            field="loss_category", other_specify_field="loss_category_other"
        )


class LossToFollowupForm(
    SiteModelFormMixin,
    FormValidatorMixin,
    ActionItemFormMixin,
    BaseModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = LossToFollowupFormValidator

    class Meta(ActionItemFormMixin.Meta):
        model = LossToFollowup
        fields = "__all__"
