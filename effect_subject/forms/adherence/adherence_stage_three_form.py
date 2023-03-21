from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_model_form.mixins import InlineModelFormMixin

from ...models import AdherenceStageThree


class AdherenceStageThreeFormValidator(FormValidator):
    pass


class AdherenceStageThreeForm(InlineModelFormMixin, CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = AdherenceStageThreeFormValidator

    def clean(self):
        cleaned_data = super().clean()
        self.unique_inline_values_or_raise(
            field="day_missed",
            inline_model="effect_subject.fluconmisseddoses",
            field_label="Fluconazole day missed",
        )
        self.validate_flucon_d1_and_d15_not_both_filled(
            field="day_missed",
            inline_model="effect_subject.fluconmisseddoses",
            field_label="Fluconazole day missed",
        )
        self.unique_inline_values_or_raise(
            field="day_missed",
            inline_model="effect_subject.flucytmisseddoses",
            field_label="Flucytosine day missed",
        )
        return cleaned_data

    def validate_flucon_d1_and_d15_not_both_filled(
        self,
        field: str = None,
        inline_model: str = None,
        field_label: str = None,
    ) -> None:
        self.field_exists_or_raise(field, inline_model)
        inline_set = f"{inline_model.split('.')[1]}_set"
        items = self.get_inline_field_values(field=field, inline_set=inline_set)
        if "1" in items and "15" in items:
            field_label = field_label or field
            raise forms.ValidationError(
                f"{field_label}: Invalid. Cannot have missed doses on both "
                "`Day 1` and `Day 15` (of 14 day fluconazole treatment intervention)."
            )

    class Meta:
        model = AdherenceStageThree
        fields = "__all__"
