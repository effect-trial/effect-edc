from dataclasses import dataclass
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import time_machine
from dateutil.relativedelta import relativedelta
from django import forms
from django.conf import settings
from django.contrib.sites.models import Site
from django.test import TestCase, tag
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_lab.models import Panel
from edc_reportable import (
    ALREADY_REPORTED,
    GRADE3,
    GRADE4,
    MILLIMOLES_PER_LITER,
    PERCENT,
    PRESENT_AT_BASELINE,
    TEN_X_9_PER_LITER,
)
from edc_reportable.units import MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_LITER
from edc_utils import convert_php_dateformat, get_utcnow
from edc_visit_schedule.constants import DAY01, DAY03, DAY09

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms import BloodResultsChemForm, BloodResultsFbcForm
from effect_subject.forms.lab_results.blood_results_chem_form import (
    BloodResultsChemFormValidator,
)
from effect_subject.forms.lab_results.blood_results_fbc_form import (
    BloodResultsFbcFormValidator,
)
from effect_subject.models import BloodResultsChem, BloodResultsFbc, SubjectRequisition


@dataclass
class LabPanelResultTestConfig:
    """Lab panel result model, form and form validator."""

    model: Any
    form: Any
    form_validator: Any

    @property
    def name(self):
        return self.model.lab_panel.name

    def __repr__(self):
        return self.name


@time_machine.travel(datetime(2023, 1, 10, 8, 00, tzinfo=ZoneInfo("UTC")))
@tag("lab")
class TestLabResults(EffectTestCaseMixin, TestCase):
    def setUp(self) -> None:
        screening_datetime = get_utcnow() - relativedelta(years=1)
        self.subject_screening = self.get_subject_screening(
            report_datetime=screening_datetime,
            eligibility_datetime=screening_datetime,
            cd4_date=(screening_datetime - relativedelta(days=7)).date(),
            serum_crag_date=(screening_datetime - relativedelta(days=6)).date(),
        )
        self.subject_consent = self.get_subject_consent(
            subject_screening=self.subject_screening,
            dob=self.subject_screening.eligibility_datetime
            - relativedelta(years=self.subject_screening.age_in_years),
        )

        self.lab_panel_test_cases = [
            LabPanelResultTestConfig(
                model=BloodResultsChem,
                form=BloodResultsChemForm,
                form_validator=BloodResultsChemFormValidator,
            ),
            LabPanelResultTestConfig(
                model=BloodResultsFbc,
                form=BloodResultsFbcForm,
                form_validator=BloodResultsFbcFormValidator,
            ),
        ]

    @staticmethod
    def get_panel_results_data(subject_visit, panel_name: str):
        requisition = SubjectRequisition.objects.create(
            subject_visit=subject_visit,
            requisition_datetime=subject_visit.report_datetime,
            panel=Panel.objects.get(name=panel_name),
        )
        return dict(
            subject_visit=subject_visit,
            requisition=requisition,
            report_datetime=subject_visit.report_datetime,
            assay_datetime=requisition.requisition_datetime + relativedelta(days=1),
            results_abnormal=NO,
            results_reportable=NOT_APPLICABLE,
            site=Site.objects.get(id=settings.SITE_ID).id,
        )

    @staticmethod
    def format_visit_date(subject_visit):
        return subject_visit.report_datetime.date().strftime(
            convert_php_dateformat(settings.SHORT_DATE_FORMAT)
        )

    def test_data_ok(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        for lab_panel in self.lab_panel_test_cases:
            with self.subTest(lab_panel=lab_panel):
                panel_results_data = self.get_panel_results_data(subject_visit, lab_panel.name)

                form = lab_panel.form(panel_results_data)
                self.assertTrue(
                    form.is_valid(),
                    f"Expected form to be valid. Got: {form.errors.as_data()}",
                )

                form_validator = lab_panel.form_validator(
                    cleaned_data=panel_results_data, model=lab_panel.model
                )
                try:
                    form_validator.validate()
                except forms.ValidationError as e:
                    self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_report_datetime_lte_7_days_ok(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        for lab_panel in self.lab_panel_test_cases:
            requisition = SubjectRequisition.objects.create(
                subject_visit=subject_visit,
                requisition_datetime=subject_visit.report_datetime,
                panel=Panel.objects.get(name=lab_panel.name),
            )
            for days in [0, 1, 2, 6, 7]:
                with self.subTest(lab_panel=lab_panel, days=days):
                    cleaned_data = dict(
                        subject_visit=subject_visit,
                        requisition=requisition,
                        report_datetime=subject_visit.report_datetime
                        + relativedelta(days=days),
                        assay_datetime=requisition.requisition_datetime
                        + relativedelta(days=1),
                        results_abnormal=NO,
                        results_reportable=NOT_APPLICABLE,
                        site=Site.objects.get(id=settings.SITE_ID).id,
                    )

                    form = lab_panel.form(cleaned_data)
                    self.assertTrue(
                        form.is_valid(),
                        f"Expected form to be valid. Got: {form.errors.as_data()}",
                    )

                    form_validator = lab_panel.form_validator(
                        cleaned_data=cleaned_data, model=lab_panel.model
                    )
                    try:
                        form_validator.validate()
                    except forms.ValidationError as e:
                        self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_report_datetime_gt_7_days_invalid(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        for lab_panel in self.lab_panel_test_cases:
            requisition = SubjectRequisition.objects.create(
                subject_visit=subject_visit,
                requisition_datetime=subject_visit.report_datetime,
                panel=Panel.objects.get(name=lab_panel.name),
            )
            for days in [8, 9, 21, 365]:
                with self.subTest(lab_panel=lab_panel, days=days):
                    cleaned_data = dict(
                        subject_visit=subject_visit,
                        requisition=requisition,
                        report_datetime=subject_visit.report_datetime
                        + relativedelta(days=days),
                        assay_datetime=requisition.requisition_datetime
                        + relativedelta(days=1),
                        results_abnormal=NO,
                        results_reportable=NOT_APPLICABLE,
                    )

                    form = lab_panel.form(cleaned_data)
                    self.assertFalse(form.is_valid(), "Form unexpectedly valid.")

                    self.assertIn("report_datetime", form.errors)
                    self.assertEqual(
                        [
                            "Report datetime may not be more than 7 days greater than "
                            "the visit report datetime. "
                            "Got 7 days."
                            "Visit report datetime is "
                            f"{self.format_visit_date(subject_visit)}. "
                            "See also AppConfig.report_datetime_allowance."
                        ],
                        form.errors.get("report_datetime"),
                    )

    def test_d1_report_datetime_before_consent_datetime_invalid(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        for lab_panel in self.lab_panel_test_cases:
            requisition = SubjectRequisition.objects.create(
                subject_visit=subject_visit,
                requisition_datetime=subject_visit.report_datetime,
                panel=Panel.objects.get(name=lab_panel.name),
            )
            for days in [-1, -2, -10, -30]:
                with self.subTest(lab_panel=lab_panel, days=days):
                    cleaned_data = dict(
                        subject_visit=subject_visit,
                        requisition=requisition,
                        report_datetime=subject_visit.report_datetime
                        + relativedelta(days=days),
                        assay_datetime=requisition.requisition_datetime
                        + relativedelta(days=1),
                        results_abnormal=NO,
                        results_reportable=NOT_APPLICABLE,
                    )

                    form = lab_panel.form(cleaned_data)
                    self.assertFalse(form.is_valid(), "Form unexpectedly valid.")

                    self.assertIn("report_datetime", form.errors)
                    self.assertIn(
                        "Consent not configured to update any previous versions.",
                        str(form.errors.get("report_datetime")),
                    )

    def test_d9_report_datetime_before_consent_datetime_invalid(self):
        self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY03,
            appt_datetime=self.subject_consent.consent_datetime + relativedelta(days=2),
        )
        subject_visit_d9 = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY09,
            appt_datetime=self.subject_consent.consent_datetime + relativedelta(days=8),
        )
        for lab_panel in self.lab_panel_test_cases:
            requisition = SubjectRequisition.objects.create(
                subject_visit=subject_visit_d9,
                requisition_datetime=subject_visit_d9.report_datetime,
                panel=Panel.objects.get(name=lab_panel.name),
            )
            for days in [-11, -10, -9]:
                with self.subTest(lab_panel=lab_panel, days=days):
                    cleaned_data = dict(
                        subject_visit=subject_visit_d9,
                        requisition=requisition,
                        report_datetime=subject_visit_d9.report_datetime
                        + relativedelta(days=days),
                        assay_datetime=requisition.requisition_datetime
                        + relativedelta(days=1),
                        results_abnormal=NO,
                        results_reportable=NOT_APPLICABLE,
                    )
                    form = lab_panel.form(cleaned_data)
                    self.assertFalse(form.is_valid(), "Form unexpectedly valid.")

                    self.assertIn("report_datetime", form.errors)
                    self.assertIn(
                        "Consent not configured to update any previous versions.",
                        str(form.errors.get("report_datetime")),
                    )

    def test_d9_report_datetime_before_visit_datetime_invalid(self):
        self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY03,
            appt_datetime=self.subject_consent.consent_datetime + relativedelta(days=2),
        )
        subject_visit_d9 = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY09,
            appt_datetime=self.subject_consent.consent_datetime + relativedelta(days=8),
        )

        for lab_panel in self.lab_panel_test_cases:
            requisition = SubjectRequisition.objects.create(
                subject_visit=subject_visit_d9,
                requisition_datetime=subject_visit_d9.report_datetime,
                panel=Panel.objects.get(name=lab_panel.name),
            )
            for days in [-8, -7, -2, -1]:
                with self.subTest(lab_panel=lab_panel, days=days):
                    cleaned_data = dict(
                        subject_visit=subject_visit_d9,
                        requisition=requisition,
                        report_datetime=subject_visit_d9.report_datetime
                        + relativedelta(days=days),
                        assay_datetime=requisition.requisition_datetime
                        + relativedelta(days=1),
                        results_abnormal=NO,
                        results_reportable=NOT_APPLICABLE,
                    )
                    form = lab_panel.form(cleaned_data)
                    self.assertFalse(form.is_valid(), "Form unexpectedly valid.")

                    self.assertIn("report_datetime", form.errors)
                    self.assertEqual(
                        [
                            "Report datetime may not be before the visit report datetime. "
                            "Visit report datetime is "
                            f"{self.format_visit_date(subject_visit_d9)}. "
                        ],
                        form.errors.get("report_datetime"),
                    )

    def test_0_lte_neutrophil_value_lt_1_ok(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "fbc")
        for value in [0, 0.01, 0.02, 0.1, 0.2]:
            with self.subTest(value=value):
                panel_results_data.update(
                    {
                        "neutrophil_value": value,
                        "neutrophil_units": TEN_X_9_PER_LITER,
                        "neutrophil_abnormal": YES,
                        "neutrophil_reportable": GRADE4,
                        "results_abnormal": YES,
                        "results_reportable": YES,
                    }
                )
                form = BloodResultsFbcForm(panel_results_data)
                self.assertTrue(
                    form.is_valid(),
                    f"Expected form to be valid. Got: {form.errors.as_data()}",
                )

                form_validator = BloodResultsFbcFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsFbc
                )
                try:
                    form_validator.validate()
                except forms.ValidationError as e:
                    self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_0_lte_neutrophil_diff_value_lt_1_ok(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "fbc")
        for value in [0, 0.01, 0.02, 0.1, 0.2]:
            with self.subTest(value=value):
                panel_results_data.update(
                    {
                        "neutrophil_diff_value": value,
                        "neutrophil_diff_units": PERCENT,
                        "neutrophil_diff_abnormal": YES,
                        "neutrophil_diff_reportable": GRADE4,
                        "results_abnormal": YES,
                        "results_reportable": YES,
                    }
                )
                form = BloodResultsFbcForm(panel_results_data)
                self.assertTrue(
                    form.is_valid(),
                    f"Expected form to be valid. Got: {form.errors.as_data()}",
                )

                form_validator = BloodResultsFbcFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsFbc
                )
                try:
                    form_validator.validate()
                except forms.ValidationError as e:
                    self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_0_lte_lymphocyte_value_lt_1_ok(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "fbc")
        for value in [0, 0.01, 0.02, 0.1, 0.2]:
            with self.subTest(value=value):
                panel_results_data.update(
                    {
                        "lymphocyte_value": value,
                        "lymphocyte_units": TEN_X_9_PER_LITER,
                        "lymphocyte_abnormal": YES,
                        "lymphocyte_reportable": GRADE4,
                        "results_abnormal": YES,
                        "results_reportable": YES,
                    }
                )
                form = BloodResultsFbcForm(panel_results_data)
                self.assertTrue(
                    form.is_valid(),
                    f"Expected form to be valid. Got: {form.errors.as_data()}",
                )

                form_validator = BloodResultsFbcFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsFbc
                )
                try:
                    form_validator.validate()
                except forms.ValidationError as e:
                    self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_0_lte_lymphocyte_diff_value_lt_1_ok(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "fbc")
        for value in [0, 0.01, 0.02, 0.1, 0.2]:
            with self.subTest(value=value):
                panel_results_data.update(
                    {
                        "lymphocyte_diff_value": value,
                        "lymphocyte_diff_units": PERCENT,
                        "lymphocyte_diff_abnormal": YES,
                        "lymphocyte_diff_reportable": GRADE4,
                        "results_abnormal": YES,
                        "results_reportable": YES,
                    }
                )
                form = BloodResultsFbcForm(panel_results_data)
                self.assertTrue(
                    form.is_valid(),
                    f"Expected form to be valid. Got: {form.errors.as_data()}",
                )

                form_validator = BloodResultsFbcFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsFbc
                )
                try:
                    form_validator.validate()
                except forms.ValidationError as e:
                    self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_negative_values_lt_0_for_neutrophil_lymphocyte_raises(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "fbc")
        for result_type in ["neutrophil", "neutrophil_diff", "lymphocyte", "lymphocyte_diff"]:
            for value in [-0.01, -0.02, -0.1, -0.2, -1, -9999]:
                with self.subTest(result_type=result_type, value=value):
                    units = PERCENT if result_type.endswith("_diff") else TEN_X_9_PER_LITER
                    panel_results_data.update(
                        {
                            f"{result_type}_value": value,
                            f"{result_type}_units": units,
                            f"{result_type}_abnormal": YES,
                            f"{result_type}_reportable": GRADE4,
                            "results_abnormal": YES,
                            "results_reportable": YES,
                        }
                    )
                    form = BloodResultsFbcForm(panel_results_data)
                    self.assertFalse(form.is_valid(), "Expected form to be invalid.")
                    self.assertIn(f"{result_type}_value", form.errors)
                    self.assertEqual(
                        ["Ensure this value is greater than or equal to 0.0."],
                        form.errors.get(f"{result_type}_value"),
                    )

    def test_sodium_in_normal_range_ok(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "chemistry")
        for normal_value in [136, 140, 144, 145]:
            with self.subTest(normal_value=normal_value):
                panel_results_data.update(
                    {
                        "sodium_value": normal_value,
                        "sodium_units": MILLIMOLES_PER_LITER,
                        "sodium_abnormal": NO,
                        "sodium_reportable": NOT_APPLICABLE,
                        "results_abnormal": NO,
                        "results_reportable": NOT_APPLICABLE,
                    }
                )
                form = BloodResultsChemForm(panel_results_data)
                self.assertTrue(
                    form.is_valid(),
                    f"Expected form to be valid. Got: {form.errors.as_data()}",
                )

                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                try:
                    form_validator.validate()
                except forms.ValidationError as e:
                    self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_sodium_135_treated_as_abnormal_and_not_reportable(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "chemistry")
        panel_results_data.update(
            {
                "sodium_value": 135,
                "sodium_units": MILLIMOLES_PER_LITER,
                "sodium_abnormal": NO,
                "sodium_reportable": NOT_APPLICABLE,
                "results_abnormal": NO,
                "results_reportable": NOT_APPLICABLE,
            }
        )
        form_validator = BloodResultsChemFormValidator(
            cleaned_data=panel_results_data, model=BloodResultsChem
        )
        with self.assertRaises(forms.ValidationError) as cm:
            form_validator.validate()
        self.assertIn("sodium_value", cm.exception.error_dict)
        self.assertIn(
            "SODIUM is abnormal.",
            str(cm.exception.error_dict.get("sodium_value")),
        )

        panel_results_data.update(
            {
                "sodium_abnormal": YES,
                "sodium_reportable": NOT_APPLICABLE,
            }
        )
        form_validator = BloodResultsChemFormValidator(
            cleaned_data=panel_results_data, model=BloodResultsChem
        )
        with self.assertRaises(forms.ValidationError) as cm:
            form_validator.validate()
        self.assertIn("sodium_reportable", cm.exception.error_dict)
        self.assertIn(
            "This field is applicable",
            str(cm.exception.error_dict.get("sodium_reportable")),
        )

        for reportable_response in [GRADE3, GRADE4, ALREADY_REPORTED, PRESENT_AT_BASELINE]:
            with self.subTest(reportable_response=reportable_response):
                panel_results_data.update(
                    {
                        "sodium_abnormal": YES,
                        "sodium_reportable": reportable_response,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                with self.assertRaises(forms.ValidationError) as cm:
                    form_validator.validate()
                self.assertIn("sodium_reportable", cm.exception.error_dict)
                self.assertIn(
                    "Invalid. Expected 'No' or 'Not applicable'.",
                    str(cm.exception.error_dict.get("sodium_reportable")),
                )

        panel_results_data.update(
            {
                "sodium_value": 135,
                "sodium_units": MILLIMOLES_PER_LITER,
                "sodium_abnormal": YES,
                "sodium_reportable": NO,
                "results_abnormal": NO,
                "results_reportable": NOT_APPLICABLE,
            }
        )
        form_validator = BloodResultsChemFormValidator(
            cleaned_data=panel_results_data, model=BloodResultsChem
        )
        with self.assertRaises(forms.ValidationError) as cm:
            form_validator.validate()
        self.assertIn("results_abnormal", cm.exception.error_dict)
        self.assertIn(
            "1 of the above results is abnormal",
            str(cm.exception.error_dict.get("results_abnormal")),
        )

        panel_results_data.update(
            {
                "sodium_value": 135,
                "sodium_units": MILLIMOLES_PER_LITER,
                "sodium_abnormal": YES,
                "sodium_reportable": NO,
                "results_abnormal": YES,
                "results_reportable": NOT_APPLICABLE,
            }
        )
        form_validator = BloodResultsChemFormValidator(
            cleaned_data=panel_results_data, model=BloodResultsChem
        )
        with self.assertRaises(forms.ValidationError) as cm:
            form_validator.validate()
        self.assertIn("results_reportable", cm.exception.error_dict)
        self.assertIn(
            "This field is applicable",
            str(cm.exception.error_dict.get("results_reportable")),
        )

        panel_results_data.update(
            {
                "results_abnormal": YES,
                "results_reportable": YES,
            }
        )
        form_validator = BloodResultsChemFormValidator(
            cleaned_data=panel_results_data, model=BloodResultsChem
        )
        with self.assertRaises(forms.ValidationError) as cm:
            form_validator.validate()
        self.assertIn("results_reportable", cm.exception.error_dict)
        self.assertIn(
            "None of the above results are reportable",
            str(cm.exception.error_dict.get("results_reportable")),
        )

        panel_results_data.update(
            {
                "results_abnormal": YES,
                "results_reportable": NO,
            }
        )
        form_validator = BloodResultsChemFormValidator(
            cleaned_data=panel_results_data, model=BloodResultsChem
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_sodium_abnormal_not_reportable_raises_if_not_acknowledged(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "chemistry")
        for abnormal_value in [
            # abnormal (G0 low sodium)
            135,
            # abnormal (G1/G2 low sodium)
            134,
            133,
            131,
            130,
            129,
            126,
            125,
            # abnormal (G1/G2 high sodium)
            146,
            149,
            150,
            151,
            153,
        ]:
            with self.subTest(abnormal_value=abnormal_value):
                panel_results_data.update(
                    {
                        "sodium_value": abnormal_value,
                        "sodium_units": MILLIMOLES_PER_LITER,
                        "sodium_abnormal": NO,
                        "sodium_reportable": NOT_APPLICABLE,
                        "results_abnormal": NO,
                        "results_reportable": NOT_APPLICABLE,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                with self.assertRaises(forms.ValidationError) as cm:
                    form_validator.validate()
                self.assertIn("sodium_value", cm.exception.error_dict)
                self.assertIn(
                    "SODIUM is abnormal.",
                    str(cm.exception.error_dict.get("sodium_value")),
                )

                panel_results_data.update(
                    {
                        "sodium_abnormal": YES,
                        "sodium_reportable": NO,
                        "results_abnormal": YES,
                        "results_reportable": NO,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                try:
                    form_validator.validate()
                except forms.ValidationError as e:
                    self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_sodium_reportable_applicable_if_sodium_abnormal(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "chemistry")
        for abnormal_value in [
            # abnormal (G0 low sodium)
            135,
            # abnormal (G1/G2 low sodium)
            134,
            125,
            # abnormal (G1/G2 high sodium)
            146,
            153,
        ]:
            with self.subTest(abnormal_value=abnormal_value):
                panel_results_data.update(
                    {
                        "sodium_value": abnormal_value,
                        "sodium_units": MILLIMOLES_PER_LITER,
                        "sodium_abnormal": YES,
                        "sodium_reportable": NOT_APPLICABLE,
                        "results_abnormal": YES,
                        "results_reportable": NOT_APPLICABLE,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                with self.assertRaises(forms.ValidationError) as cm:
                    form_validator.validate()
                self.assertIn("sodium_reportable", cm.exception.error_dict)
                self.assertIn(
                    "This field is applicable if result is abnormal",
                    str(cm.exception.error_dict.get("sodium_reportable")),
                )

                panel_results_data.update(
                    {
                        "sodium_abnormal": YES,
                        "sodium_reportable": NO,
                        "results_abnormal": YES,
                        "results_reportable": NO,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                try:
                    form_validator.validate()
                except forms.ValidationError as e:
                    self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_sodium_reportable_raises_if_abnormal_lt_g3_and_reported_reportable(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "chemistry")
        for abnormal_value in [
            # abnormal (G0 low sodium)
            135,
            # abnormal (G1/G2 low sodium)
            134,
            125,
            # abnormal (G1/G2 high sodium)
            146,
            153,
        ]:
            for reportable_response in [
                GRADE3,
                GRADE4,
                ALREADY_REPORTED,
                PRESENT_AT_BASELINE,
            ]:
                with self.subTest(
                    abnormal_value=abnormal_value, reportable_response=reportable_response
                ):
                    panel_results_data.update(
                        {
                            "sodium_value": abnormal_value,
                            "sodium_units": MILLIMOLES_PER_LITER,
                            "sodium_abnormal": YES,
                            "sodium_reportable": reportable_response,
                            "results_abnormal": YES,
                            "results_reportable": NOT_APPLICABLE,
                        }
                    )
                    form_validator = BloodResultsChemFormValidator(
                        cleaned_data=panel_results_data, model=BloodResultsChem
                    )
                    with self.assertRaises(forms.ValidationError) as cm:
                        form_validator.validate()
                    self.assertIn("sodium_reportable", cm.exception.error_dict)
                    self.assertIn(
                        "Invalid. Expected 'No' or 'Not applicable'.",
                        str(cm.exception.error_dict.get("sodium_reportable")),
                    )

                    panel_results_data.update(
                        {
                            "sodium_abnormal": YES,
                            "sodium_reportable": NO,
                            "results_abnormal": YES,
                            "results_reportable": NO,
                        }
                    )
                    form_validator = BloodResultsChemFormValidator(
                        cleaned_data=panel_results_data, model=BloodResultsChem
                    )
                    try:
                        form_validator.validate()
                    except forms.ValidationError as e:
                        self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_sodium_g3_raises_if_not_acknowledged(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "chemistry")
        for g3_value in [
            # G3 (low sodium)
            121,
            122,
            123,
            124,
            # G3 (high sodium)
            154,
            155,
            158,
            159,
        ]:
            for reportable_response in [NOT_APPLICABLE, NO, GRADE4]:
                with self.subTest(g3_value=g3_value, reportable_response=reportable_response):
                    panel_results_data.update(
                        {
                            "sodium_value": g3_value,
                            "sodium_units": MILLIMOLES_PER_LITER,
                            "sodium_abnormal": NO,
                            "sodium_reportable": reportable_response,
                            "results_abnormal": NO,
                            "results_reportable": NOT_APPLICABLE,
                        }
                    )
                    form_validator = BloodResultsChemFormValidator(
                        cleaned_data=panel_results_data, model=BloodResultsChem
                    )
                    with self.assertRaises(forms.ValidationError) as cm:
                        form_validator.validate()
                    self.assertIn("sodium_value", cm.exception.error_dict)
                    self.assertIn(
                        "SODIUM is reportable.",
                        str(cm.exception.error_dict.get("sodium_value")),
                    )
                    self.assertIn(
                        "GRADE 3.",
                        str(cm.exception.error_dict.get("sodium_value")),
                    )

                panel_results_data.update(
                    {
                        "sodium_abnormal": NO,
                        "sodium_reportable": GRADE3,
                        "results_abnormal": NO,
                        "results_reportable": NOT_APPLICABLE,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                with self.assertRaises(forms.ValidationError) as cm:
                    form_validator.validate()
                self.assertIn("sodium_value", cm.exception.error_dict)
                self.assertIn(
                    "SODIUM is abnormal.",
                    str(cm.exception.error_dict.get("sodium_value")),
                )

                panel_results_data.update(
                    {
                        "sodium_abnormal": YES,
                        "sodium_reportable": GRADE3,
                        "results_abnormal": NO,
                        "results_reportable": NOT_APPLICABLE,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                with self.assertRaises(forms.ValidationError) as cm:
                    form_validator.validate()
                self.assertIn("results_abnormal", cm.exception.error_dict)
                self.assertIn(
                    "1 of the above results is abnormal",
                    str(cm.exception.error_dict.get("results_abnormal")),
                )

                panel_results_data.update(
                    {
                        "sodium_abnormal": YES,
                        "sodium_reportable": GRADE3,
                        "results_abnormal": YES,
                        "results_reportable": NOT_APPLICABLE,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                with self.assertRaises(forms.ValidationError) as cm:
                    form_validator.validate()
                self.assertIn("results_reportable", cm.exception.error_dict)
                self.assertIn(
                    "This field is applicable.",
                    str(cm.exception.error_dict.get("results_reportable")),
                )

                panel_results_data.update(
                    {
                        "sodium_abnormal": YES,
                        "sodium_reportable": GRADE3,
                        "results_abnormal": YES,
                        "results_reportable": NO,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                with self.assertRaises(forms.ValidationError) as cm:
                    form_validator.validate()
                self.assertIn("results_reportable", cm.exception.error_dict)
                self.assertIn(
                    "1 of the above results is reportable",
                    str(cm.exception.error_dict.get("results_reportable")),
                )

                panel_results_data.update(
                    {
                        "sodium_abnormal": YES,
                        "sodium_reportable": GRADE3,
                        "results_abnormal": YES,
                        "results_reportable": YES,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                try:
                    form_validator.validate()
                except forms.ValidationError as e:
                    self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_sodium_g4_raises_if_not_acknowledged(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "chemistry")
        for g4_value in [
            # G4 (low sodium)
            120,
            119,
            110,
            100,
            # G4 (high sodium)
            160,
            161,
            170,
            200,
        ]:
            for reportable_response in [NOT_APPLICABLE, NO, GRADE3]:
                with self.subTest(g4_value=g4_value, reportable_response=reportable_response):
                    panel_results_data.update(
                        {
                            "sodium_value": g4_value,
                            "sodium_units": MILLIMOLES_PER_LITER,
                            "sodium_abnormal": NO,
                            "sodium_reportable": reportable_response,
                            "results_abnormal": NO,
                            "results_reportable": NOT_APPLICABLE,
                        }
                    )
                    form_validator = BloodResultsChemFormValidator(
                        cleaned_data=panel_results_data, model=BloodResultsChem
                    )
                    with self.assertRaises(forms.ValidationError) as cm:
                        form_validator.validate()
                    self.assertIn("sodium_value", cm.exception.error_dict)
                    self.assertIn(
                        "SODIUM is reportable.",
                        str(cm.exception.error_dict.get("sodium_value")),
                    )
                    self.assertIn(
                        "GRADE 4.",
                        str(cm.exception.error_dict.get("sodium_value")),
                    )

                panel_results_data.update(
                    {
                        "sodium_abnormal": NO,
                        "sodium_reportable": GRADE4,
                        "results_abnormal": NO,
                        "results_reportable": NOT_APPLICABLE,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                with self.assertRaises(forms.ValidationError) as cm:
                    form_validator.validate()
                self.assertIn("sodium_value", cm.exception.error_dict)
                self.assertIn(
                    "SODIUM is abnormal.",
                    str(cm.exception.error_dict.get("sodium_value")),
                )

                panel_results_data.update(
                    {
                        "sodium_abnormal": YES,
                        "sodium_reportable": GRADE4,
                        "results_abnormal": NO,
                        "results_reportable": NOT_APPLICABLE,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                with self.assertRaises(forms.ValidationError) as cm:
                    form_validator.validate()
                self.assertIn("results_abnormal", cm.exception.error_dict)
                self.assertIn(
                    "1 of the above results is abnormal",
                    str(cm.exception.error_dict.get("results_abnormal")),
                )

                panel_results_data.update(
                    {
                        "sodium_abnormal": YES,
                        "sodium_reportable": GRADE4,
                        "results_abnormal": YES,
                        "results_reportable": NOT_APPLICABLE,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                with self.assertRaises(forms.ValidationError) as cm:
                    form_validator.validate()
                self.assertIn("results_reportable", cm.exception.error_dict)
                self.assertIn(
                    "This field is applicable.",
                    str(cm.exception.error_dict.get("results_reportable")),
                )

                panel_results_data.update(
                    {
                        "sodium_abnormal": YES,
                        "sodium_reportable": GRADE4,
                        "results_abnormal": YES,
                        "results_reportable": NO,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                with self.assertRaises(forms.ValidationError) as cm:
                    form_validator.validate()
                self.assertIn("results_reportable", cm.exception.error_dict)
                self.assertIn(
                    "1 of the above results is reportable",
                    str(cm.exception.error_dict.get("results_reportable")),
                )

                panel_results_data.update(
                    {
                        "sodium_abnormal": YES,
                        "sodium_reportable": GRADE4,
                        "results_abnormal": YES,
                        "results_reportable": YES,
                    }
                )
                form_validator = BloodResultsChemFormValidator(
                    cleaned_data=panel_results_data, model=BloodResultsChem
                )
                try:
                    form_validator.validate()
                except forms.ValidationError as e:
                    self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_negative_crp_values_lt_0_raises(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "fbc")
        for value in [-0.01, -0.02, -0.1, -0.2, -1, -9999]:
            for units in [MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_LITER]:
                with self.subTest(value=value, units=units):
                    panel_results_data.update(
                        {
                            "crp_value": value,
                            "crp_units": units,
                            "crp_abnormal": NO,
                            "crp_reportable": NOT_APPLICABLE,
                            "results_abnormal": NO,
                            "results_reportable": NOT_APPLICABLE,
                        }
                    )
                    form = BloodResultsChemForm(panel_results_data)
                    self.assertFalse(form.is_valid(), "Expected form to be invalid.")
                    self.assertIn("crp_value", form.errors)
                    self.assertEqual(
                        ["Ensure this value is greater than or equal to 0.0."],
                        form.errors.get("crp_value"),
                    )

    def test_crp_in_normal_range_ok(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "chemistry")
        for normal_value in [0, 0.1, 1, 3, 4, 4.9, 5]:
            for units in [MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_LITER]:
                with self.subTest(normal_value=normal_value, units=units):
                    panel_results_data.update(
                        {
                            "crp_value": (
                                normal_value
                                if units == MILLIGRAMS_PER_LITER
                                else round(normal_value / 10, 2)
                            ),
                            "crp_units": units,
                            "crp_abnormal": NO,
                            "crp_reportable": NOT_APPLICABLE,
                            "results_abnormal": NO,
                            "results_reportable": NOT_APPLICABLE,
                        }
                    )

                    form = BloodResultsChemForm(panel_results_data)
                    self.assertTrue(
                        form.is_valid(),
                        f"Expected form to be valid. Got: {form.errors.as_data()}",
                    )

                    form_validator = BloodResultsChemFormValidator(
                        cleaned_data=panel_results_data, model=BloodResultsChem
                    )
                    try:
                        form_validator.validate()
                    except forms.ValidationError as e:
                        self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_abnormal_crp_raises_if_not_acknowledged_abnormal(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "chemistry")
        for normal_value in [5.05, 5.1, 6, 10, 50, 999]:
            for units in [MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_LITER]:
                with self.subTest(normal_value=normal_value, units=units):
                    panel_results_data.update(
                        {
                            "crp_value": (
                                normal_value
                                if units == MILLIGRAMS_PER_LITER
                                else round(normal_value / 10, 2)
                            ),
                            "crp_units": units,
                            "crp_abnormal": NO,
                            "crp_reportable": NOT_APPLICABLE,
                            "results_abnormal": NO,
                            "results_reportable": NOT_APPLICABLE,
                        }
                    )
                    form = BloodResultsChemForm(panel_results_data)
                    self.assertFalse(form.is_valid(), "Expected form to be invalid.")
                    self.assertIn("crp_value", form.errors)
                    self.assertIn(
                        "CRP is abnormal. ",
                        str(form.errors.get("crp_value")),
                    )

                    form_validator = BloodResultsChemFormValidator(
                        cleaned_data=panel_results_data, model=BloodResultsChem
                    )
                    with self.assertRaises(forms.ValidationError) as cm:
                        form_validator.validate()
                    self.assertIn("crp_value", cm.exception.error_dict)
                    self.assertIn(
                        "CRP is abnormal. ",
                        str(cm.exception.error_dict.get("crp_value")),
                    )
                    self.assertIn(
                        (
                            "Normal ranges: 0.0<=x<=5.0 mg/L "
                            if units == MILLIGRAMS_PER_LITER
                            else "Normal ranges: 0.0<=x<=0.5 mg/dL"
                        ),
                        str(cm.exception.error_dict.get("crp_value")),
                    )

                    panel_results_data.update(
                        {
                            "crp_abnormal": YES,
                            "crp_reportable": NO,
                            "results_abnormal": NO,
                            "results_reportable": NO,
                        }
                    )
                    form = BloodResultsChemForm(panel_results_data)
                    self.assertFalse(form.is_valid(), "Expected form to be invalid.")
                    self.assertIn("results_abnormal", form.errors)
                    self.assertIn(
                        "1 of the above results is abnormal",
                        str(form.errors.get("results_abnormal")),
                    )

                    panel_results_data.update(
                        {
                            "crp_abnormal": YES,
                            "crp_reportable": NO,
                            "results_abnormal": YES,
                            "results_reportable": NO,
                        }
                    )
                    form = BloodResultsChemForm(panel_results_data)
                    self.assertTrue(
                        form.is_valid(),
                        f"Expected form to be valid. Got: {form.errors.as_data()}",
                    )

                    form_validator = BloodResultsChemFormValidator(
                        cleaned_data=panel_results_data, model=BloodResultsChem
                    )
                    try:
                        form_validator.validate()
                    except forms.ValidationError as e:
                        self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_abnormal_crp_not_reportable(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DAY01,
            appt_datetime=self.subject_consent.consent_datetime,
        )
        panel_results_data = self.get_panel_results_data(subject_visit, "chemistry")
        for normal_value in [5.05, 5.1, 6, 10, 50, 999]:
            for units in [MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_LITER]:
                for crp_reportable in [
                    GRADE3,
                    GRADE4,
                    ALREADY_REPORTED,
                    PRESENT_AT_BASELINE,
                ]:
                    with self.subTest(
                        normal_value=normal_value,
                        units=units,
                        crp_reportable=crp_reportable,
                    ):
                        panel_results_data.update(
                            {
                                "crp_value": (
                                    normal_value
                                    if units == MILLIGRAMS_PER_LITER
                                    else round(normal_value / 10, 2)
                                ),
                                "crp_units": units,
                                "crp_abnormal": YES,
                                "crp_reportable": NOT_APPLICABLE,
                                "results_abnormal": YES,
                                "results_reportable": NOT_APPLICABLE,
                            }
                        )
                        form_validator = BloodResultsChemFormValidator(
                            cleaned_data=panel_results_data, model=BloodResultsChem
                        )
                        with self.assertRaises(forms.ValidationError) as cm:
                            form_validator.validate()
                        self.assertIn("crp_reportable", cm.exception.error_dict)
                        self.assertIn(
                            "This field is applicable if result is abnormal",
                            str(cm.exception.error_dict.get("crp_reportable")),
                        )

                        panel_results_data.update(
                            {
                                "crp_abnormal": YES,
                                "crp_reportable": crp_reportable,
                                "results_abnormal": YES,
                                "results_reportable": NOT_APPLICABLE,
                            }
                        )
                        form_validator = BloodResultsChemFormValidator(
                            cleaned_data=panel_results_data, model=BloodResultsChem
                        )
                        with self.assertRaises(forms.ValidationError) as cm:
                            form_validator.validate()
                        self.assertIn("crp_reportable", cm.exception.error_dict)
                        self.assertIn(
                            "Invalid. Expected 'No' or 'Not applicable'.",
                            str(cm.exception.error_dict.get("crp_reportable")),
                        )

                        panel_results_data.update(
                            {
                                "crp_abnormal": YES,
                                "crp_reportable": NO,
                                "results_abnormal": YES,
                                "results_reportable": NOT_APPLICABLE,
                            }
                        )
                        form_validator = BloodResultsChemFormValidator(
                            cleaned_data=panel_results_data, model=BloodResultsChem
                        )
                        with self.assertRaises(forms.ValidationError) as cm:
                            form_validator.validate()
                        self.assertIn("results_reportable", cm.exception.error_dict)
                        self.assertIn(
                            "This field is applicable.",
                            str(cm.exception.error_dict.get("results_reportable")),
                        )

                        panel_results_data.update(
                            {
                                "crp_abnormal": YES,
                                "crp_reportable": NO,
                                "results_abnormal": YES,
                                "results_reportable": YES,
                            }
                        )
                        form_validator = BloodResultsChemFormValidator(
                            cleaned_data=panel_results_data, model=BloodResultsChem
                        )
                        with self.assertRaises(forms.ValidationError) as cm:
                            form_validator.validate()
                        self.assertIn("results_reportable", cm.exception.error_dict)
                        self.assertIn(
                            "None of the above results are reportable",
                            str(cm.exception.error_dict.get("results_reportable")),
                        )

                        panel_results_data.update(
                            {
                                "crp_abnormal": YES,
                                "crp_reportable": NO,
                                "results_abnormal": YES,
                                "results_reportable": NO,
                            }
                        )
                        form_validator = BloodResultsChemFormValidator(
                            cleaned_data=panel_results_data, model=BloodResultsChem
                        )
                        try:
                            form_validator.validate()
                        except forms.ValidationError as e:
                            self.fail(f"ValidationError unexpectedly raised. Got {e}")
