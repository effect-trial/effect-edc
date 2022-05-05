from typing import Dict

from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_constants.constants import (
    FEMALE,
    MALE,
    NEG,
    NO,
    NOT_APPLICABLE,
    PENDING,
    POS,
    YES,
)
from edc_utils.date import get_utcnow

from effect_screening.eligibility import ScreeningEligibility
from effect_screening.forms import SubjectScreeningForm
from effect_screening.models import SubjectScreening

from ..effect_test_case_mixin import EffectTestCaseMixin


@tag("elig")
class TestForms(EffectTestCaseMixin, TestCase):
    ELIGIBLE_CD4_VALUE = 99

    @staticmethod
    def get_data():
        return {
            "screening_consent": YES,
            "willing_to_participate": YES,
            "consent_ability": YES,
            "report_datetime": get_utcnow(),
            "initials": "EW",
            "gender": MALE,
            "age_in_years": 25,
        }

    @staticmethod
    def get_basic_opts():
        return {
            "screening_consent": YES,
            "willing_to_participate": YES,
            "consent_ability": YES,
            "report_datetime": get_utcnow(),
            "initials": "EW",
            "gender": FEMALE,
            "age_in_years": 25,
            "unsuitable_for_study": NO,
            "unsuitable_agreed": NOT_APPLICABLE,
            "any_other_mg_ssx_other": "",
        }

    @property
    def inclusion_criteria(self):
        return dict(
            hiv_pos=YES,
            cd4_value=self.ELIGIBLE_CD4_VALUE,
            cd4_date=(get_utcnow() - relativedelta(days=7)).date(),
            serum_crag_value=POS,
            serum_crag_date=(get_utcnow() - relativedelta(days=6)).date(),
            lp_declined=NOT_APPLICABLE,
            lp_done=YES,
            lp_date=(get_utcnow() - relativedelta(days=6)).date(),
            csf_crag_value=NEG,
        )

    @property
    def exclusion_criteria(self):
        return dict(
            contraindicated_meds=NO,
            cm_in_csf=NO,
            cm_in_csf_method=NOT_APPLICABLE,
            mg_severe_headache=NO,
            mg_headache_nuchal_rigidity=NO,
            mg_headache_vomiting=NO,
            mg_seizures=NO,
            mg_gcs_lt_15=NO,
            any_other_mg_ssx=NO,
            jaundice=NO,
            on_fluconazole=NO,
            pregnant=NOT_APPLICABLE,
            breast_feeding=NO,
            prior_cm_episode=NO,
            reaction_to_study_drugs=NO,
        )

    def get_valid_opts(self) -> Dict:
        return dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )

    def test_screening_ok(self):
        opts = {
            "screening_consent": YES,
            "willing_to_participate": YES,
            "consent_ability": YES,
            "report_datetime": get_utcnow(),
            "initials": "EW",
            "gender": MALE,
            "age_in_years": 25,
        }
        SubjectScreening.objects.create(**opts)
        form = SubjectScreeningForm(initial=self.get_data(), instance=SubjectScreening())
        form.is_valid()

    def test_basic_eligibility(self):
        obj = SubjectScreening.objects.create(**self.get_basic_opts())
        self.assertFalse(obj.eligible)
        self.assertIn("incomplete inclusion criteria", obj.reasons_ineligible.lower())
        self.assertIn("incomplete exclusion criteria", obj.reasons_ineligible.lower())

    def test_inclusion_criteria_for_eligibility(self):
        instance = SubjectScreening.objects.create(
            **self.inclusion_criteria, **self.get_basic_opts()
        )
        obj = ScreeningEligibility(instance)
        self.assertFalse(obj.is_eligible)
        self.assertNotIn("inclusion_criteria", obj.reasons_ineligible)

    def test_exclusion_criteria_for_eligibility(self):
        model_obj = SubjectScreening.objects.create(
            **self.exclusion_criteria, **self.get_basic_opts()
        )
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertFalse(obj.is_eligible)
        self.assertNotIn("exclusion_criteria", obj.reasons_ineligible)

    def test_criteria_for_eligibility(self):
        model_obj = SubjectScreening.objects.create(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({}, obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)

    def test_mg_ssx_ineligible(self):
        for mg_ssx in [
            "mg_severe_headache",
            "mg_headache_nuchal_rigidity",
            "mg_headache_vomiting",
            "mg_seizures",
            "mg_gcs_lt_15",
            "any_other_mg_ssx",
        ]:
            with self.subTest(mg_ssx=mg_ssx):
                model_obj = SubjectScreening.objects.create(
                    **self.inclusion_criteria,
                    **self.exclusion_criteria,
                    **self.get_basic_opts(),
                )
                setattr(model_obj, mg_ssx, YES)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertFalse(obj.is_eligible)
                self.assertDictEqual(
                    {mg_ssx: "Signs of symptomatic meningitis"},
                    obj.reasons_ineligible,
                )

                setattr(model_obj, mg_ssx, NO)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertTrue(obj.is_eligible)
                self.assertDictEqual({}, obj.reasons_ineligible)

    def test_valid_opts_ok(self):
        form = SubjectScreeningForm(data=self.get_valid_opts())
        form.is_valid()
        self.assertDictEqual({}, form._errors)

    @tag("preg")
    def test_male_preg_raises(self):
        opts = dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        opts.update(
            gender=MALE,
            pregnant=YES,
            breast_feeding=NOT_APPLICABLE,
            unsuitable_for_study=NO,
            unsuitable_agreed=NOT_APPLICABLE,
            lp_declined=NOT_APPLICABLE,
        )
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("pregnant", form._errors)

        opts.update(pregnant=NO)
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("pregnant", form._errors)

        opts.update(pregnant=NOT_APPLICABLE, preg_test_date=get_utcnow().date())
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("preg_test_date", form._errors)

        opts.update(pregnant=NOT_APPLICABLE, preg_test_date=None, breast_feeding=YES)
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("breast_feeding", form._errors)

        opts.update(
            pregnant=NOT_APPLICABLE, preg_test_date=None, breast_feeding=NOT_APPLICABLE
        )
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertDictEqual({}, form._errors)

    @tag("preg")
    def test_female_preg_or_bf(self):
        opts = dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        opts.update(
            gender=FEMALE,
            pregnant=NOT_APPLICABLE,
            breast_feeding=NOT_APPLICABLE,
        )
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("pregnant", form._errors)
        self.assertIn("breast_feeding", form._errors)

        opts.update(
            gender=FEMALE,
            pregnant=YES,
            preg_test_date=get_utcnow(),
            breast_feeding=NOT_APPLICABLE,
        )
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("pregnant", form._errors)
        self.assertNotIn("preg_test_date", form._errors)
        self.assertIn("breast_feeding", form._errors)

        opts.update(
            gender=FEMALE,
            pregnant=YES,
            preg_test_date=get_utcnow(),
            breast_feeding=YES,
        )
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("pregnant", form._errors)
        self.assertNotIn("preg_test_date", form._errors)
        self.assertNotIn("breast_feeding", form._errors)

        opts.update(
            gender=FEMALE,
            pregnant=YES,
            preg_test_date=None,
            breast_feeding=YES,
        )
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("pregnant", form._errors)
        self.assertNotIn("preg_test_date", form._errors)
        self.assertNotIn("breast_feeding", form._errors)

    def test_crags_and_lp(self):
        # TODO: Is this ok?
        opts = dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        opts.update(lp_done=PENDING)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertEqual(obj.reasons_ineligible, {})
        self.assertTrue(obj.is_eligible)

    def test_eligible_cd4_values_ok(self):
        opts = self.get_valid_opts()
        eligible_cd4_values = [0, 1, 80, 99]
        for cd4_value in eligible_cd4_values:
            with self.subTest(cd4_value=cd4_value):
                opts.update(cd4_value=cd4_value)
                form = SubjectScreeningForm(data=opts)
                form.is_valid()
                self.assertDictEqual({}, form._errors)

    def test_ineligible_cd4_value_raises_validation_error(self):
        opts = self.get_valid_opts()
        ineligible_cd4_values = [-1, 100, 120, 200]
        for cd4_value in ineligible_cd4_values:
            with self.subTest(cd4_value=cd4_value):
                opts.update(cd4_value=cd4_value)
                form = SubjectScreeningForm(data=opts)
                form.is_valid()
                self.assertIn("cd4_value", form._errors)
                self.assertDictEqual(
                    {
                        "cd4_value": [
                            "Ensure this value is less than or equal to 99."
                            if cd4_value > 0
                            else "Ensure this value is greater than or equal to 0."
                        ]
                    },
                    form._errors,
                )
        opts.update(cd4_value=self.ELIGIBLE_CD4_VALUE)
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertDictEqual({}, form._errors)

    def test_cd4_value_required(self):
        opts = self.get_valid_opts()
        for cd4_value in [None, ""]:
            with self.subTest(cd4_value=cd4_value):
                opts.update(cd4_value=cd4_value)

                form = SubjectScreeningForm(data=opts)
                form.is_valid()
                self.assertIn("cd4_value", form._errors)
                self.assertDictEqual({"cd4_value": ["This field is required."]}, form._errors)

    def test_cd4_date_within_21_days(self):
        opts = dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        report_datetime = opts.get("report_datetime")
        opts.update(cd4_date=report_datetime - relativedelta(days=22))
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("cd4_date", form._errors)

        opts.update(cd4_date=report_datetime - relativedelta(days=7))
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("cd4_date", form._errors)
        self.assertDictEqual({}, form._errors)

    def test_serum_crag_negative_raises_validation_error(self):
        opts = self.get_valid_opts()
        opts.update(serum_crag_value=NEG)
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("serum_crag_value", form._errors)
        self.assertDictEqual(
            {
                "serum_crag_value": [
                    "Invalid. " "Subject must have positive serum/plasma CrAg test result."
                ]
            },
            form._errors,
        )

    def test_serum_crag_date_required(self):
        opts = self.get_valid_opts()
        opts.update(serum_crag_date="")
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("serum_crag_date", form._errors)
        self.assertDictEqual(
            {"serum_crag_date": ["This field is required."]},
            form._errors,
        )

        opts.update(serum_crag_date=opts.get("lp_date"))
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("serum_crag_date", form._errors)
        self.assertDictEqual({}, form._errors)

    def test_serum_crag_date_within_14_days(self):
        opts = self.get_valid_opts()
        report_datetime = opts.get("report_datetime")
        cd4_date = report_datetime - relativedelta(days=20)

        opts.update(
            cd4_date=cd4_date,
            serum_crag_date=report_datetime - relativedelta(days=14 + 1),
        )
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("serum_crag_date", form._errors)
        self.assertDictEqual(
            {
                "serum_crag_date": [
                    "Invalid. Cannot be more than 14 days before the report date"
                ]
            },
            form._errors,
        )

        opts.update(
            cd4_date=cd4_date,
            serum_crag_date=report_datetime - relativedelta(days=14),
        )
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("cd4_date", form._errors)
        self.assertDictEqual({}, form._errors)

        opts.update(
            cd4_date=cd4_date,
            serum_crag_date=report_datetime - relativedelta(days=14 - 1),
        )
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("cd4_date", form._errors)
        self.assertDictEqual({}, form._errors)

    def test_serum_crag_date_not_before_cd4_date(self):
        opts = dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        report_datetime = opts.get("report_datetime")
        opts.update(cd4_date=report_datetime - relativedelta(days=7))
        opts.update(serum_crag_date=report_datetime - relativedelta(days=14))
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("serum_crag_date", form._errors)

        opts.update(cd4_date=report_datetime - relativedelta(days=7))
        opts.update(serum_crag_date=report_datetime - relativedelta(days=6))
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertDictEqual({}, form._errors)

    def test_age(self):
        opts = dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        opts.update(age_in_years=2)
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("age_in_years", form._errors)

        opts.update(age_in_years=18)
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("age_in_years", form._errors)

    def test_cm_in_csf(self):
        opts = dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        opts.update(cm_in_csf=YES)

        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("cm_in_csf", form._errors)

        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertIn("cm_in_csf", obj.reasons_ineligible)
        self.assertFalse(obj.is_eligible)

        opts.update(cm_in_csf=NO)

        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertNotIn("cm_in_csf", obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)

    def test_any_other_mg_ssx_other(self):
        opts = self.get_valid_opts()
        opts.update(any_other_mg_ssx=YES, any_other_mg_ssx_other="")

        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("any_other_mg_ssx_other", form._errors)
        self.assertDictEqual(
            {"any_other_mg_ssx_other": ["This field is required."]}, form._errors
        )

        opts.update(any_other_mg_ssx=YES, any_other_mg_ssx_other="Some other sx")

        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("any_other_mg_ssx_other", form._errors)
        self.assertDictEqual({}, form._errors)
