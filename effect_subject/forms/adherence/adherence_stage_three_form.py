from django import forms
from edc_constants.constants import NOT_REQUIRED
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

        self.validate_flucon_d15_against_d1()

        self.unique_inline_values_or_raise(
            field="day_missed",
            inline_model="effect_subject.flucytmisseddoses",
            field_label="Flucytosine day missed",
        )
        return cleaned_data

    def validate_flucon_d15_against_d1(self) -> None:
        inline_model = "effect_subject.fluconmisseddoses"
        inline_set = f"{inline_model.split('.')[1]}_set"
        total_forms = int(self.data.get(f"{inline_set}-TOTAL_FORMS"))
        day_15_answered = False
        day_1_set_to_protocol_not_required = False

        for i in range(0, total_forms):
            if self.data.get(f"{inline_set}-{i}-DELETE") == "on":
                pass
            else:
                day_missed_field = f"{inline_set}-{i}-day_missed"
                missed_reason_field = f"{inline_set}-{i}-missed_reason"

                if self.data[day_missed_field] == "15":
                    day_15_answered = True
                elif (
                    self.data[day_missed_field] == "1"
                    and self.data[missed_reason_field] == NOT_REQUIRED
                ):
                    day_1_set_to_protocol_not_required = True

        if day_15_answered and not day_1_set_to_protocol_not_required:
            raise forms.ValidationError(
                "Fluconazole day missed: Invalid. `Day 15` dose only applicable "
                "if `Day 1` is `Not required according to protocol`."
            )

    class Meta:
        model = AdherenceStageThree
        fields = "__all__"
