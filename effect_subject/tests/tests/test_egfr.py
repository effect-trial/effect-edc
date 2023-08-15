from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django import forms
from django.test import TestCase
from edc_constants.constants import FEMALE, NO, NOT_APPLICABLE, YES
from edc_egfr.calculators import EgfrCalculatorError
from edc_lab.models import Panel
from edc_reportable import MICROMOLES_PER_LITER
from edc_utils import age
from edc_visit_schedule.constants import DAY1

from effect_consent.models import SubjectConsent
from effect_screening.models import SubjectScreening
from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms.lab_results.blood_results_chem_form import (
    BloodResultsChemFormValidator,
)
from effect_subject.models import BloodResultsChem, SubjectRequisition, VitalSigns


class TestEgfr(EffectTestCaseMixin, TestCase):
    def setUp(self) -> None:
        self.subject_visit = self.get_subject_visit(
            visit_code=DAY1, gender=FEMALE, age_in_years=33
        )
        panel = Panel.objects.get(name=BloodResultsChem.lab_panel.name)
        self.requisition = SubjectRequisition.objects.create(
            subject_visit=self.subject_visit,
            report_datetime=self.subject_visit.report_datetime,
            panel=panel,
        )

    @staticmethod
    def create_vital_signs(subject_visit, weight=None):
        return VitalSigns.objects.create(
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            weight=weight,
            weight_measured_or_est="measured",
            abnormal_lung_exam=NO,
            heart_rate=45,
            patient_admitted=NOT_APPLICABLE,
            reportable_as_ae=NO,
            respiratory_rate=35,
            temperature=37.1,
        )

    def test_assert_values_for_these_tests(self):
        obj = SubjectScreening.objects.get(
            subject_identifier=self.subject_visit.subject_identifier
        )
        self.assertEqual(33, obj.age_in_years)
        self.assertEqual(FEMALE, obj.gender)
        obj = SubjectConsent.objects.get(
            subject_identifier=self.subject_visit.subject_identifier
        )
        self.assertEqual(
            33, age(obj.dob, reference_dt=self.subject_visit.report_datetime).years
        )

    def test_saves_ok_without_creatinine_value(self):
        obj = BloodResultsChem(
            subject_visit=self.subject_visit,
            requisition=self.requisition,
            report_datetime=self.subject_visit.report_datetime,
            assay_datetime=self.requisition.report_datetime + relativedelta(days=1),
        )
        # creatinine not entered
        try:
            obj.save()
        except EgfrCalculatorError:
            self.fail("EgfrCalculatorError unexpectedly raised")
        # egfr_value is None
        self.assertIsNone(obj.egfr_value)

    def test_raise_on_missing_weight(self):
        obj = BloodResultsChem(
            subject_visit=self.subject_visit,
            requisition=self.requisition,
            report_datetime=self.subject_visit.report_datetime,
            assay_datetime=self.requisition.report_datetime + relativedelta(days=1),
            creatinine_value=Decimal("100.0"),
            creatinine_units=MICROMOLES_PER_LITER,
        )
        # creatinine entered, no weight from vital signs. need both!
        self.assertRaises(EgfrCalculatorError, obj.save)

    def test_ok(self):
        obj = BloodResultsChem(
            subject_visit=self.subject_visit,
            requisition=self.requisition,
            report_datetime=self.subject_visit.report_datetime,
            assay_datetime=self.requisition.report_datetime + relativedelta(days=1),
            creatinine_value=Decimal("100.0"),
            creatinine_units=MICROMOLES_PER_LITER,
        )
        self.create_vital_signs(self.subject_visit, weight=80)
        # creatinine entered and have weight from vital signs, ok.
        try:
            obj.save()
        except EgfrCalculatorError:
            self.fail("EgfrCalculatorError unexpectedly raised")

        self.assertEqual(round(obj.egfr_value), 90)

    def test_no_vital_signs_at_this_visit_but_exist_at_previous_visit_ok(self):
        subject_visit_d3 = self.get_next_subject_visit(subject_visit=self.subject_visit)
        requisition_d3 = SubjectRequisition.objects.create(
            subject_visit=subject_visit_d3,
            report_datetime=subject_visit_d3.report_datetime,
            panel=Panel.objects.get(name=BloodResultsChem.lab_panel.name),
        )
        obj = BloodResultsChem(
            subject_visit=subject_visit_d3,
            requisition=requisition_d3,
            report_datetime=subject_visit_d3.report_datetime,
            assay_datetime=requisition_d3.report_datetime + relativedelta(days=1),
            creatinine_value=Decimal("100.0"),
            creatinine_units=MICROMOLES_PER_LITER,
        )
        # creatinine entered and no weight from vital signs raises
        self.assertRaises(EgfrCalculatorError, obj.save)

        # create vital signs at previous visit, and retest
        self.create_vital_signs(self.subject_visit, weight=80)
        try:
            obj.save()
        except EgfrCalculatorError:
            self.fail("EgfrCalculatorError unexpectedly raised")

        self.assertEqual(round(obj.egfr_value), 90)

        # create vital signs at this visit, and retest
        self.create_vital_signs(subject_visit_d3, weight=60)
        try:
            obj.save()
        except EgfrCalculatorError:
            self.fail("EgfrCalculatorError unexpectedly raised")

        self.assertEqual(round(obj.egfr_value), 67)

    def test_form_validator(self):
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            requisition=self.requisition,
            report_datetime=self.subject_visit.report_datetime,
            assay_datetime=self.requisition.report_datetime + relativedelta(days=1),
            results_abnormal=NO,
            results_reportable=NOT_APPLICABLE,
        )
        form_validator = BloodResultsChemFormValidator(
            cleaned_data=cleaned_data, model=BloodResultsChem
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

        # add creatinine
        cleaned_data = dict(
            subject_visit=self.subject_visit,
            requisition=self.requisition,
            report_datetime=self.subject_visit.report_datetime,
            assay_datetime=self.requisition.report_datetime + relativedelta(days=1),
            creatinine_value=Decimal("100.0"),
            creatinine_units=MICROMOLES_PER_LITER,
            creatinine_abnormal=YES,
            creatinine_reportable=NO,
            results_abnormal=YES,
            results_reportable=NO,
        )
        form_validator = BloodResultsChemFormValidator(
            cleaned_data=cleaned_data, model=BloodResultsChem
        )
        with self.assertRaises(forms.ValidationError) as cm:
            form_validator.validate()
        self.assertIn("Participant weight not found", str(cm.exception))

        # add weight with vital signs
        self.create_vital_signs(self.subject_visit, weight=80)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")
