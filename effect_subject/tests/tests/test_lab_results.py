from dataclasses import dataclass
from typing import Any

from dateutil.relativedelta import relativedelta
from django import forms
from django.conf import settings
from django.test import TestCase
from edc_constants.constants import NO, NOT_APPLICABLE
from edc_lab.models import Panel
from edc_utils import convert_php_dateformat, formatted_datetime, get_utcnow
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


class TestLabResults(EffectTestCaseMixin, TestCase):
    def setUp(self) -> None:
        screening_datetime = get_utcnow() - relativedelta(years=1)
        self.subject_screening = self.get_subject_screening(
            report_datetime=screening_datetime,
            eligibility_datetime=screening_datetime,
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
                    self.assertEqual(
                        [
                            "Invalid. Cannot be before date of consent. "
                            "Participant consent on "
                            f"{formatted_datetime(self.subject_consent.consent_datetime)}"
                        ],
                        form.errors.get("report_datetime"),
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
                    self.assertEqual(
                        [
                            "Invalid. Cannot be before date of consent. "
                            "Participant consent on "
                            f"{formatted_datetime(self.subject_consent.consent_datetime)}"
                        ],
                        form.errors.get("report_datetime"),
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
