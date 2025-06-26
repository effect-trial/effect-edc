from django import forms
from django.utils.safestring import mark_safe
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_egfr.form_validator_mixins import EgfrCockcroftGaultFormValidatorMixin
from edc_form_validators import INVALID_ERROR
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin
from edc_registration.models import RegisteredSubject
from edc_utils import age

from ...models import BloodResultsChem, VitalSigns
from ...utils import get_weight_in_kgs


class BloodResultsChemFormValidator(
    BloodResultsFormValidatorMixin, EgfrCockcroftGaultFormValidatorMixin, CrfFormValidator
):
    panel = BloodResultsChem.lab_panel

    def get_weight_in_kgs(self) -> float | None:
        obj = (
            VitalSigns.objects.filter(subject_visit=self.related_visit, weight__isnull=False)
            .order_by("report_datetime")
            .last()
        )
        if obj:
            return obj.weight
        return None

    def datetime_in_window_or_raise(self, *args):
        pass

    def clean(self) -> None:
        if self.cleaned_data.get("creatinine_value") and not get_weight_in_kgs(
            subject_visit=self.related_visit
        ):
            self.raise_validation_error(
                "Participant weight not found. Please complete the Vital Signs CRF first.",
                INVALID_ERROR,
            )
        if self.cleaned_data.get("creatinine_value") and self.cleaned_data.get(
            "creatinine_units"
        ):

            rs = RegisteredSubject.objects.get(
                subject_identifier=self.related_visit.subject_identifier
            )
            age_in_years = age(rs.dob, self.report_datetime).years

            self.validate_egfr(
                gender=rs.gender,
                age_in_years=age_in_years,
                ethnicity=rs.ethnicity,
                weight_in_kgs=self.get_weight_in_kgs(),
            )
        super().clean()


class BloodResultsChemForm(ActionItemCrfFormMixin, CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = BloodResultsChemFormValidator

    report_datetime_allowance = 7

    class Meta(ActionItemCrfFormMixin.Meta):
        model = BloodResultsChem
        fields = "__all__"
        help_texts = {
            "action_identifier": "(read-only)",
            "egfr_value": mark_safe(  # nosec B308
                "Calculated using Cockcroft-Gault equation. "
                "See https://www.mdcalc.com/creatinine-clearance-cockcroft-gault-equation"
            ),
        }
