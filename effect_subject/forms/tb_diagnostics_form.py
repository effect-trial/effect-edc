from django import forms
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.extra_mixins import StudyDayFormValidatorMixin
from edc_microbiology.form_validators import (
    BloodCultureFormValidatorMixin,
    HistopathologyFormValidatorMixin,
    SputumAfbFormValidatorMixin,
    SputumCultureFormValidatorMixin,
    SputumGenexpertFormValidatorMixin,
    UrinaryLamFormValidatorMixin,
)

from ..models import TbDiagnostics


class TbDiagnosticsFormValidator(
    StudyDayFormValidatorMixin,
    UrinaryLamFormValidatorMixin,
    SputumGenexpertFormValidatorMixin,
    SputumCultureFormValidatorMixin,
    SputumAfbFormValidatorMixin,
    BloodCultureFormValidatorMixin,
    HistopathologyFormValidatorMixin,
    CrfFormValidator,
):
    def clean(self):
        self.validate_study_day_with_datetime(
            subject_identifier=self.cleaned_data.get("subject_visit").subject_identifier,
            study_day=self.cleaned_data.get("day_blood_taken"),
            compare_date=self.cleaned_data.get("blood_taken_date"),
            study_day_field="day_blood_taken",
        )

        self.validate_study_day_with_datetime(
            subject_identifier=self.cleaned_data.get("subject_visit").subject_identifier,
            study_day=self.cleaned_data.get("day_biopsy_taken"),
            compare_date=self.cleaned_data.get("biopsy_date"),
            study_day_field="day_biopsy_taken",
        )

        self.validate_urinary_lam()

        self.validate_sputum_genexpert()
        self.validate_sputum_culture()
        self.validate_sputum_afb()

        self.validate_blood_culture()

        self.validate_histopathology()

    def validate_sputum_afb(self):
        self.applicable_if_true(
            self.cleaned_data.get("sputum_requisition"),
            field_applicable="sputum_culture_performed",
        )
        return super().validate_sputum_afb()

    def validate_sputum_culture(self):
        self.applicable_if_true(
            self.cleaned_data.get("sputum_requisition"),
            field_applicable="sputum_afb_performed",
        )
        return super().validate_sputum_culture()

    def validate_sputum_genexpert(self):
        self.applicable_if_true(
            self.cleaned_data.get("sputum_requisition"),
            field_applicable="sputum_genexpert_performed",
        )
        return super().validate_sputum_genexpert()


class TbDiagnosticsForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = TbDiagnosticsFormValidator

    class Meta:
        model = TbDiagnostics
        fields = "__all__"
