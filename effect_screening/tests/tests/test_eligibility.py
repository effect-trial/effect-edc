from typing import Dict

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.sites.models import Site
from django.test import TestCase, tag
from edc_constants.constants import (
    FEMALE,
    INCOMPLETE,
    MALE,
    NEG,
    NO,
    NOT_APPLICABLE,
    NOT_DONE,
    NOT_EVALUATED,
    NOT_TESTED,
    PENDING,
    POS,
    YES,
)
from edc_utils.date import get_utcnow

from effect_screening.eligibility import (
    INCOMPLETE_EXCLUSION,
    INCOMPLETE_INCLUSION,
    ScreeningEligibility,
)
from effect_screening.forms import SubjectScreeningForm
from effect_screening.models import SubjectScreening

from ..effect_test_case_mixin import EffectTestCaseMixin


@tag("elig")
class TestEligibility(EffectTestCaseMixin, TestCase):
    """Subject screening eligibility tests.

    For form validation tests, see also:
        effect_form_validators/tests/effect_screening/test_subject_screening.py
    """

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
            "site": Site.objects.get(id=settings.SITE_ID),
            "screening_consent": YES,
            "willing_to_participate": YES,
            "consent_ability": YES,
            "report_datetime": get_utcnow(),
            "initials": "EW",
            "gender": FEMALE,
            "age_in_years": 25,
            "parent_guardian_consent": NOT_APPLICABLE,
            "hiv_confirmed_date": (get_utcnow() - relativedelta(days=28)).date(),
            "hiv_confirmed_method": "historical_lab_result",
            "unsuitable_for_study": NO,
            "unsuitable_reason": NOT_APPLICABLE,
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
            on_flucon=NO,
            pregnant=NOT_APPLICABLE,
            breast_feeding=NO,
            prior_cm_episode=NO,
            reaction_to_study_drugs=NO,
        )

    def get_eligible_opts(self) -> Dict:
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
        self.assertEqual(YES, obj.eligible)
        self.assertEqual("ELIGIBLE", obj.display_label)

    def test_valid_opts_eligible(self):
        obj = SubjectScreening.objects.create(**self.get_eligible_opts())

        elig_obj = ScreeningEligibility(model_obj=obj)
        self.assertDictEqual({}, elig_obj.reasons_ineligible)
        self.assertTrue(elig_obj.is_eligible)
        self.assertEqual(YES, elig_obj.eligible)
        self.assertEqual("ELIGIBLE", elig_obj.display_label)

    def test_valid_opts_ok(self):
        form = SubjectScreeningForm(data=self.get_eligible_opts())
        form.is_valid()
        self.assertDictEqual({}, form._errors)

    def test_inclusion_age_lt_18_ineligible(self):
        for age_in_years in [-1, 0, 1, 10, 12, 15, 17]:
            for consent_answ in [YES, NO, NOT_APPLICABLE]:
                with self.subTest(age_in_years=age_in_years, consent_answ=consent_answ):
                    opts = self.get_eligible_opts()
                    opts.update(
                        age_in_years=age_in_years,
                        parent_guardian_consent=consent_answ,
                    )
                    model_obj = SubjectScreening.objects.create(**opts)
                    obj = ScreeningEligibility(model_obj=model_obj)
                    self.assertDictEqual(
                        {"age_in_years": "Age not >= 18"}, obj.reasons_ineligible
                    )
                    self.assertFalse(obj.is_eligible)
                    self.assertEqual(NO, obj.eligible)
                    self.assertEqual("INELIGIBLE", obj.display_label)

    def test_inclusion_age_gte_18_ok(self):
        for age_in_years in [18, 19, 30, 60, 99, 110]:
            with self.subTest(age_in_years=age_in_years):
                opts = self.get_eligible_opts()
                opts.update(age_in_years=age_in_years)
                model_obj = SubjectScreening.objects.create(**opts)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertDictEqual({}, obj.reasons_ineligible)
                self.assertTrue(obj.is_eligible)
                self.assertEqual(YES, obj.eligible)
                self.assertEqual("ELIGIBLE", obj.display_label)

    def test_inclusion_hiv_pos_no_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(hiv_pos=NO)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({"hiv_pos": "Not HIV sero-positive"}, obj.reasons_ineligible)
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_inclusion_hiv_pos_yes_ok(self):
        opts = self.get_eligible_opts()
        opts.update(hiv_pos=YES)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({}, obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)
        self.assertEqual(YES, obj.eligible)
        self.assertEqual("ELIGIBLE", obj.display_label)

    def test_inclusion_cd4_gte_100_ineligible(self):
        ineligible_cd4_values = [100, 101, 120, 200]
        for cd4_value in ineligible_cd4_values:
            with self.subTest(cd4_value=cd4_value):
                opts = self.get_eligible_opts()
                opts.update(cd4_value=cd4_value)
                model_obj = SubjectScreening.objects.create(**opts)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertDictEqual(
                    {"cd4_value": "CD4 not <100 cells/μL"}, obj.reasons_ineligible
                )
                self.assertFalse(obj.is_eligible)
                self.assertEqual(NO, obj.eligible)
                self.assertEqual("INELIGIBLE", obj.display_label)

    def test_inclusion_cd4_lt_100_ok(self):
        eligible_cd4_values = [0, 1, 80, 99]
        for cd4_value in eligible_cd4_values:
            with self.subTest(cd4_value=cd4_value):
                opts = self.get_eligible_opts()
                opts.update(cd4_value=cd4_value)
                model_obj = SubjectScreening.objects.create(**opts)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertDictEqual({}, obj.reasons_ineligible)
                self.assertTrue(obj.is_eligible)
                self.assertEqual(YES, obj.eligible)
                self.assertEqual("ELIGIBLE", obj.display_label)

    def test_inclusion_cd4_date_gt_60_days_ineligible(self):
        for days_ago in [61, 62, 100, 365]:
            with self.subTest(days_ago=days_ago):
                opts = self.get_eligible_opts()
                report_datetime = opts.get("report_datetime")
                cd4_date = report_datetime.date() - relativedelta(days=days_ago)
                opts.update(cd4_date=cd4_date)
                model_obj = SubjectScreening.objects.create(**opts)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertDictEqual({"cd4_date": "CD4 > 60 days"}, obj.reasons_ineligible)
                self.assertFalse(obj.is_eligible)
                self.assertEqual(NO, obj.eligible)
                self.assertEqual("INELIGIBLE", obj.display_label)

    def test_inclusion_cd4_date_lte_60_days_ok(self):
        for days_ago in [0, 1, 7, 14, 15, 20, 21, 59, 60]:
            with self.subTest(days_ago=days_ago):
                opts = self.get_eligible_opts()
                report_datetime = opts.get("report_datetime")
                cd4_date = report_datetime.date() - relativedelta(days=days_ago)
                opts.update(cd4_date=cd4_date)
                model_obj = SubjectScreening.objects.create(**opts)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertDictEqual({}, obj.reasons_ineligible)
                self.assertTrue(obj.is_eligible)
                self.assertEqual(YES, obj.eligible)
                self.assertEqual("ELIGIBLE", obj.display_label)

    def test_inclusion_serum_crag_date_gt_21_days_ineligible(self):
        for days_ago in [-99, -30, -23, -22, 22, 23, 30, 99]:
            with self.subTest(days_ago=days_ago):
                opts = self.get_eligible_opts()
                report_datetime = opts.get("report_datetime")
                cd4_date = report_datetime.date() - relativedelta(days=20)
                opts.update(
                    cd4_date=cd4_date,
                    serum_crag_date=report_datetime.date() - relativedelta(days=days_ago),
                )
                model_obj = SubjectScreening.objects.create(**opts)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertDictEqual(
                    {"serum_crag_date": "Serum CrAg > 21 days"},
                    obj.reasons_ineligible,
                )
                self.assertFalse(obj.is_eligible)
                self.assertEqual(NO, obj.eligible)
                self.assertEqual("INELIGIBLE", obj.display_label)

    def test_inclusion_serum_crag_date_lte_21_days_ok(self):
        for days_ago in [-21, -20, -14, -13, -1, 0, 1, 13, 14, 20, 21]:
            with self.subTest(days_ago=days_ago):
                opts = self.get_eligible_opts()
                report_datetime = opts.get("report_datetime")
                cd4_date = report_datetime.date() - relativedelta(days=20)
                opts.update(
                    cd4_date=cd4_date,
                    serum_crag_date=report_datetime.date() - relativedelta(days=days_ago),
                )
                model_obj = SubjectScreening.objects.create(**opts)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertDictEqual({}, obj.reasons_ineligible)
                self.assertTrue(obj.is_eligible)
                self.assertEqual(YES, obj.eligible)
                self.assertEqual("ELIGIBLE", obj.display_label)

    def test_inclusion_csf_crag_value_pending_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(
            lp_done=YES,
            lp_date=(get_utcnow() - relativedelta(days=6)).date(),
            csf_crag_value=PENDING,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({"csf_crag_value": "CSF CrAg pending"}, obj.reasons_ineligible)
        self.assertFalse(obj.is_eligible)
        self.assertEqual(PENDING, obj.eligible)
        self.assertEqual("PENDING", obj.display_label)

    def test_inclusion_csf_crag_value_positive_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(
            lp_done=YES,
            lp_date=(get_utcnow() - relativedelta(days=6)).date(),
            csf_crag_value=POS,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({"csf_crag_value": "CSF CrAg (+)"}, obj.reasons_ineligible)
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_inclusion_csf_crag_value_not_done_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(
            lp_done=YES,
            lp_date=(get_utcnow() - relativedelta(days=6)).date(),
            csf_crag_value=NOT_DONE,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {
                "lp_done": "LP done",
                "csf_crag_value": "CSF CrAg not done",
            },
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_inclusion_csf_crag_value_negative_ok(self):
        opts = self.get_eligible_opts()
        opts.update(csf_crag_value=NEG)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({}, obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)
        self.assertEqual(YES, obj.eligible)
        self.assertEqual("ELIGIBLE", obj.display_label)

    def test_inclusion_lp_done_no_lp_declined_no_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(
            lp_done=NO,
            lp_date=None,
            lp_declined=NO,
            csf_crag_value=NOT_APPLICABLE,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertEqual(
            {
                "lp_done": "LP not done",
                "lp_declined": "LP not declined",
            },
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_inclusion_lp_done_no_lp_declined_yes_ok(self):
        opts = self.get_eligible_opts()
        opts.update(
            lp_done=NO,
            lp_date=None,
            lp_declined=YES,
            csf_crag_value=NOT_APPLICABLE,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({}, obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)
        self.assertEqual(YES, obj.eligible)
        self.assertEqual("ELIGIBLE", obj.display_label)

    def test_inclusion_willing_to_participate_no_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(willing_to_participate=NO)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertEqual(
            {"willing_to_participate": "Unwilling to participate"}, obj.reasons_ineligible
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_inclusion_willing_to_participate_yes_ok(self):
        opts = self.get_eligible_opts()
        opts.update(willing_to_participate=YES)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({}, obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)
        self.assertEqual(YES, obj.eligible)
        self.assertEqual("ELIGIBLE", obj.display_label)

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
            preg_test_date=get_utcnow().date(),
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
            preg_test_date=get_utcnow().date(),
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

    def test_eligible_cd4_values_ok(self):
        opts = self.get_eligible_opts()
        eligible_cd4_values = [0, 1, 80, 99]
        for cd4_value in eligible_cd4_values:
            with self.subTest(cd4_value=cd4_value):
                opts.update(cd4_value=cd4_value)
                form = SubjectScreeningForm(data=opts)
                form.is_valid()
                self.assertDictEqual({}, form._errors)

    def test_ineligible_cd4_value_raises_validation_error(self):
        opts = self.get_eligible_opts()
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
                            (
                                "Ensure this value is less than or equal to 99."
                                if cd4_value > 0
                                else "Ensure this value is greater than or equal to 0."
                            )
                        ]
                    },
                    form._errors,
                )
        opts.update(cd4_value=self.ELIGIBLE_CD4_VALUE)
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertDictEqual({}, form._errors)

    def test_cd4_value_required(self):
        opts = self.get_eligible_opts()
        for cd4_value in [None, ""]:
            with self.subTest(cd4_value=cd4_value):
                opts.update(cd4_value=cd4_value)

                form = SubjectScreeningForm(data=opts)
                form.is_valid()
                self.assertIn("cd4_value", form._errors)
                self.assertDictEqual({"cd4_value": ["This field is required."]}, form._errors)

    def test_form_allows_cd4_date_over_21_days(self):
        opts = dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        report_datetime = opts.get("report_datetime")

        for days_ago in [7, 21, 59, 60, 61, 100, 365]:
            with self.subTest(days_ago=days_ago):
                opts.update(cd4_date=report_datetime.date() - relativedelta(days=days_ago))
                form = SubjectScreeningForm(data=opts)
                form.is_valid()
                self.assertNotIn("cd4_date", form._errors)
                self.assertDictEqual({}, form._errors)

    def test_serum_crag_negative_raises_validation_error(self):
        opts = self.get_eligible_opts()
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
        opts = self.get_eligible_opts()
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

    def test_serum_crag_date_can_be_before_cd4_date(self):
        opts = dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        report_datetime = opts.get("report_datetime")
        opts.update(
            cd4_date=report_datetime.date() - relativedelta(days=7),
            serum_crag_date=report_datetime.date() - relativedelta(days=14),
        )
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertDictEqual({}, form._errors)

    def test_serum_crag_date_can_be_after_cd4_date(self):
        opts = dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        report_datetime = opts.get("report_datetime")
        opts.update(
            cd4_date=report_datetime.date() - relativedelta(days=7),
            serum_crag_date=report_datetime.date() - relativedelta(days=6),
        )
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertDictEqual({}, form._errors)

    def test_age(self):
        opts = dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        opts.update(age_in_years=-1)
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("age_in_years", form._errors)

        opts.update(age_in_years=120)
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("age_in_years", form._errors)

        opts.update(age_in_years=18)
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("age_in_years", form._errors)

        opts.update(age_in_years=12, parent_guardian_consent=YES)
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
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

        opts.update(cm_in_csf=NO)

        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertNotIn("cm_in_csf", obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)
        self.assertEqual(YES, obj.eligible)
        self.assertEqual("ELIGIBLE", obj.display_label)

    def test_any_other_mg_ssx_other(self):
        opts = self.get_eligible_opts()
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

    def test_exclusion_prior_cm_episode_yes_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(prior_cm_episode=YES)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {"prior_cm_episode": "Prior episode of CM"}, obj.reasons_ineligible
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_exclusion_prior_cm_episode_no_ok(self):
        opts = self.get_eligible_opts()
        opts.update(prior_cm_episode=NO)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({}, obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)
        self.assertEqual(YES, obj.eligible)
        self.assertEqual("ELIGIBLE", obj.display_label)

    def test_exclusion_pregnant_yes_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(
            gender=FEMALE,
            pregnant=YES,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({"pregnant": "Pregnant"}, obj.reasons_ineligible)
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_exclusion_pregnant_no_ok(self):
        for answ in [NO, NOT_APPLICABLE]:
            with self.subTest(pregnant=answ):
                opts = self.get_eligible_opts()
                opts.update(
                    gender=FEMALE,
                    pregnant=NO,
                )
                model_obj = SubjectScreening.objects.create(**opts)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertDictEqual({}, obj.reasons_ineligible)
                self.assertTrue(obj.is_eligible)
                self.assertEqual(YES, obj.eligible)
                self.assertEqual("ELIGIBLE", obj.display_label)

    def test_exclusion_breast_feeding_yes_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(
            gender=FEMALE,
            breast_feeding=YES,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({"breast_feeding": "Breastfeeding"}, obj.reasons_ineligible)
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_exclusion_breast_feeding_no_ok(self):
        opts = self.get_eligible_opts()
        opts.update(
            gender=FEMALE,
            breast_feeding=NO,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({}, obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)
        self.assertEqual(YES, obj.eligible)
        self.assertEqual("ELIGIBLE", obj.display_label)

    def test_exclusion_reaction_to_study_drugs_yes_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(reaction_to_study_drugs=YES)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {"reaction_to_study_drugs": "Serious reaction to flucytosine or fluconazole"},
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_exclusion_reaction_to_study_drugs_no_ok(self):
        opts = self.get_eligible_opts()
        opts.update(reaction_to_study_drugs=NO)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({}, obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)
        self.assertEqual(YES, obj.eligible)
        self.assertEqual("ELIGIBLE", obj.display_label)

    def test_exclusion_on_flucon_yes_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(on_flucon=YES)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({"on_flucon": "On fluconazole"}, obj.reasons_ineligible)
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_exclusion_on_flucon_no_ok(self):
        opts = self.get_eligible_opts()
        opts.update(on_flucon=NO)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({}, obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)
        self.assertEqual(YES, obj.eligible)
        self.assertEqual("ELIGIBLE", obj.display_label)

    def test_exclusion_contraindicated_meds_yes_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(contraindicated_meds=YES)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {"contraindicated_meds": "Contraindicated concomitant medications"},
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_exclusion_contraindicated_meds_no_ok(self):
        opts = self.get_eligible_opts()
        opts.update(contraindicated_meds=NO)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({}, obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)
        self.assertEqual(YES, obj.eligible)
        self.assertEqual("ELIGIBLE", obj.display_label)

    def test_exclusion_mg_ssx_yes_ineligible(self):
        for mg_ssx in [
            "mg_severe_headache",
            "mg_headache_nuchal_rigidity",
            "mg_headache_vomiting",
            "mg_seizures",
            "mg_gcs_lt_15",
            "any_other_mg_ssx",
        ]:
            with self.subTest(mg_ssx=mg_ssx):
                opts = self.get_eligible_opts()
                opts.update({mg_ssx: YES})
                model_obj = SubjectScreening.objects.create(**opts)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertFalse(obj.is_eligible)
                self.assertEqual(NO, obj.eligible)
                self.assertEqual("INELIGIBLE", obj.display_label)

                self.assertDictEqual(
                    {mg_ssx: "Signs of symptomatic meningitis"},
                    obj.reasons_ineligible,
                )

                opts.update({mg_ssx: NO})
                model_obj = SubjectScreening.objects.create(**opts)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertDictEqual({}, obj.reasons_ineligible)
                self.assertTrue(obj.is_eligible)
                self.assertEqual(YES, obj.eligible)
                self.assertEqual("ELIGIBLE", obj.display_label)

    def test_exclusion_mg_ssx_no_ok(self):
        for mg_ssx in [
            "mg_severe_headache",
            "mg_headache_nuchal_rigidity",
            "mg_headache_vomiting",
            "mg_seizures",
            "mg_gcs_lt_15",
            "any_other_mg_ssx",
        ]:
            with self.subTest(mg_ssx=mg_ssx):
                opts = self.get_eligible_opts()
                opts.update({mg_ssx: NO})
                model_obj = SubjectScreening.objects.create(**opts)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertDictEqual({}, obj.reasons_ineligible)
                self.assertTrue(obj.is_eligible)
                self.assertEqual(YES, obj.eligible)
                self.assertEqual("ELIGIBLE", obj.display_label)

    def test_exclusion_jaundice_yes_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(jaundice=YES)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({"jaundice": "Jaundice"}, obj.reasons_ineligible)
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_exclusion_jaundice_no_ok(self):
        opts = self.get_eligible_opts()
        opts.update(jaundice=NO)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({}, obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)
        self.assertEqual(YES, obj.eligible)
        self.assertEqual("ELIGIBLE", obj.display_label)

    def test_exclusion_cm_in_csf_yes_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(cm_in_csf=YES)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {"cm_in_csf": "Positive evidence of CM on CSF"}, obj.reasons_ineligible
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_exclusion_cm_in_csf_not_yes_ok(self):
        for answ in [NO, PENDING, NOT_TESTED, NOT_APPLICABLE]:
            with self.subTest(cm_in_csf=answ):
                opts = self.get_eligible_opts()
                opts.update(cm_in_csf=answ)
                model_obj = SubjectScreening.objects.create(**opts)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertDictEqual({}, obj.reasons_ineligible)
                self.assertTrue(obj.is_eligible)
                self.assertEqual(YES, obj.eligible)
                self.assertEqual("ELIGIBLE", obj.display_label)

    def test_consent_ability_no_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(consent_ability=NO)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {"consent_ability": "Incapable of consenting"}, obj.reasons_ineligible
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_consent_ability_yes_ok(self):
        opts = self.get_eligible_opts()
        opts.update(consent_ability=YES)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({}, obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)
        self.assertEqual(YES, obj.eligible)
        self.assertEqual("ELIGIBLE", obj.display_label)

    def test_unsuitable_for_study_yes_ineligible(self):
        opts = self.get_eligible_opts()
        opts.update(unsuitable_for_study=YES)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {"unsuitable_for_study": "Deemed unsuitable other reason"}, obj.reasons_ineligible
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_unsuitable_for_study_no_ok(self):
        opts = self.get_eligible_opts()
        opts.update(unsuitable_for_study=NO)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({}, obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)
        self.assertEqual(YES, obj.eligible)
        self.assertEqual("ELIGIBLE", obj.display_label)

    def test_inclusion_answer_not_evaluated_ineligible(self):
        for fld in [
            "hiv_pos",
            "willing_to_participate",
            "consent_ability",
        ]:
            with self.subTest(fld=fld):
                opts = self.get_eligible_opts()
                opts.update({fld: NOT_EVALUATED})
                model_obj = SubjectScreening.objects.create(**opts)
                obj = ScreeningEligibility(model_obj=model_obj)
                self.assertDictEqual(
                    {"inclusion_criteria": "Incomplete inclusion criteria"},
                    obj.reasons_ineligible,
                )
                self.assertFalse(obj.is_eligible)
                self.assertEqual(INCOMPLETE, obj.eligible)
                self.assertEqual(INCOMPLETE, obj.display_label)

    def test_exclusion_answer_not_evaluated_ineligible(self):
        for fld in [
            "prior_cm_episode",
            "reaction_to_study_drugs",
            "on_flucon",
            "contraindicated_meds",
            "mg_severe_headache",
            "mg_headache_nuchal_rigidity",
            "mg_headache_vomiting",
            "mg_seizures",
            "mg_gcs_lt_15",
            "any_other_mg_ssx",
            "pregnant",
            "breast_feeding",
            "unsuitable_for_study",
            "jaundice",
        ]:
            with self.subTest(fld=fld):
                opts = self.get_eligible_opts()
                opts.update({fld: NOT_EVALUATED})
                model_obj = SubjectScreening.objects.create(**opts)
                obj = ScreeningEligibility(model_obj=model_obj)

                self.assertDictEqual(
                    {"exclusion_criteria": "Incomplete exclusion criteria"},
                    obj.reasons_ineligible,
                )
                self.assertFalse(obj.is_eligible)
                self.assertEqual(INCOMPLETE, obj.eligible)
                self.assertEqual(INCOMPLETE, obj.display_label)

    def test_assessment_is_incomplete_true_if_reasons_ineligible_all_incomplete(self):
        for reasons_ineligible in (
            {"inclusion_criteria": INCOMPLETE_INCLUSION},
            {"exclusion_criteria": INCOMPLETE_EXCLUSION},
            {
                "inclusion_criteria": INCOMPLETE_INCLUSION,
                "exclusion_criteria": INCOMPLETE_EXCLUSION,
            },
            {
                "exclusion_criteria": INCOMPLETE_EXCLUSION,
                "inclusion_criteria": INCOMPLETE_INCLUSION,
            },
        ):
            with self.subTest(reasons_ineligible=reasons_ineligible):
                self.assertTrue(
                    ScreeningEligibility.assessment_is_incomplete(reasons_ineligible)
                )

    def test_assessment_is_incomplete_false_if_reasons_ineligible_empty(self):
        self.assertFalse(ScreeningEligibility.assessment_is_incomplete({}))

    def test_assessment_is_incomplete_false_if_reasons_ineligible_not_all_incomplete(self):
        for reasons_ineligible in (
            {"inclusion_criteria": INCOMPLETE_INCLUSION, "willing_to_participate": NO},
            {"reaction_to_study_drugs": YES, "exclusion_criteria": INCOMPLETE_EXCLUSION},
            # Failed inclusion
            {"hiv_pos": "Not HIV sero-positive"},
            {"cd4_value": "CD4 not <100 cells/μL"},
            {"csf_crag_value": "CSF CrAg pending"},
            {"csf_crag_value": "CSF CrAg (+)"},
            {"lp_done": "LP not done", "lp_declined": "LP not declined"},
            # Failed exclusion
            {"cm_in_csf": "Positive evidence of CM on CSF"},
            {"jaundice": "Jaundice"},
            {"on_flucon": "On fluconazole"},
            {"pregnant": "Pregnant"},
            {"breast_feeding": "Breastfeeding"},
            # Failed inclusion & exclusion
            {"csf_crag_value": "CSF CrAg (+)", "on_flucon": "On fluconazole"},
            {"pregnant": "Pregnant", "cd4_value": "CD4 not <100 cells/μL"},
            # Missing + pending
            {"csf_crag_value": "CSF CrAg pending", "inclusion_criteria": INCOMPLETE_INCLUSION},
            {"inclusion_criteria": INCOMPLETE_INCLUSION, "csf_crag_value": "CSF CrAg pending"},
            # Missing + failed
            {
                "inclusion_criteria": INCOMPLETE_INCLUSION,
                "exclusion_criteria": INCOMPLETE_EXCLUSION,
                "mg_severe_headache": "Signs of symptomatic meningitis",
            },
            {
                "mg_severe_headache": "Signs of symptomatic meningitis",
                "exclusion_criteria": INCOMPLETE_EXCLUSION,
                "inclusion_criteria": INCOMPLETE_INCLUSION,
            },
            {
                "mg_severe_headache": "Signs of symptomatic meningitis",
                "exclusion_criteria": INCOMPLETE_EXCLUSION,
            },
            {
                "inclusion_criteria": INCOMPLETE_INCLUSION,
                "mg_severe_headache": "Signs of symptomatic meningitis",
            },
        ):
            with self.subTest(reasons_ineligible=reasons_ineligible):
                self.assertFalse(
                    ScreeningEligibility.assessment_is_incomplete(reasons_ineligible)
                )

    def test_status_pending_if_csf_crag_value_pending(self):
        opts = self.get_eligible_opts()
        opts.update(
            lp_done=YES,
            lp_date=(get_utcnow() - relativedelta(days=6)).date(),
            csf_crag_value=PENDING,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual({"csf_crag_value": "CSF CrAg pending"}, obj.reasons_ineligible)
        self.assertFalse(obj.is_eligible)
        self.assertEqual(PENDING, obj.eligible)
        self.assertEqual("PENDING", obj.display_label)

    def test_status_pending_if_csf_crag_value_pending_and_failed_inclusion_criteria(self):
        opts = self.get_eligible_opts()
        opts.update(
            willing_to_participate=NO,
            lp_done=YES,
            lp_date=(get_utcnow() - relativedelta(days=6)).date(),
            csf_crag_value=PENDING,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertEqual(
            {
                "csf_crag_value": "CSF CrAg pending",
                "willing_to_participate": "Unwilling to participate",
            },
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(PENDING, obj.eligible)
        self.assertEqual("PENDING", obj.display_label)

    def test_status_pending_if_csf_crag_value_pending_and_failed_exclusion_criteria(self):
        opts = self.get_eligible_opts()
        opts.update(
            prior_cm_episode=YES,
            lp_done=YES,
            lp_date=(get_utcnow() - relativedelta(days=6)).date(),
            csf_crag_value=PENDING,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertEqual(
            {
                "prior_cm_episode": "Prior episode of CM",
                "csf_crag_value": "CSF CrAg pending",
            },
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(PENDING, obj.eligible)
        self.assertEqual("PENDING", obj.display_label)

    def test_status_pending_if_csf_crag_value_pending_and_inclusion_criteria_incomplete(self):
        opts = self.get_eligible_opts()
        opts.update(
            hiv_pos=NOT_EVALUATED,
            hiv_confirmed_date=None,
            hiv_confirmed_method=NOT_APPLICABLE,
            lp_done=YES,
            lp_date=(get_utcnow() - relativedelta(days=6)).date(),
            csf_crag_value=PENDING,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertEqual(
            {
                "inclusion_criteria": INCOMPLETE_INCLUSION,
                "csf_crag_value": "CSF CrAg pending",
            },
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(PENDING, obj.eligible)
        self.assertEqual("PENDING", obj.display_label)

    def test_status_pending_if_csf_crag_value_pending_and_exclusion_criteria_incomplete(self):
        opts = self.get_eligible_opts()
        opts.update(
            jaundice=NOT_EVALUATED,
            lp_done=YES,
            lp_date=(get_utcnow() - relativedelta(days=6)).date(),
            csf_crag_value=PENDING,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertEqual(
            {
                "csf_crag_value": "CSF CrAg pending",
                "exclusion_criteria": INCOMPLETE_EXCLUSION,
            },
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(PENDING, obj.eligible)
        self.assertEqual("PENDING", obj.display_label)

    def test_status_pending_if_csf_crag_value_pending_and_incl_excl_criteria_incomplete(self):
        opts = self.get_eligible_opts()
        opts.update(
            hiv_pos=NOT_EVALUATED,
            hiv_confirmed_date=None,
            hiv_confirmed_method=NOT_APPLICABLE,
            prior_cm_episode=NOT_EVALUATED,
            lp_done=YES,
            lp_date=(get_utcnow() - relativedelta(days=6)).date(),
            csf_crag_value=PENDING,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertEqual(
            {
                "csf_crag_value": "CSF CrAg pending",
                "exclusion_criteria": INCOMPLETE_EXCLUSION,
                "inclusion_criteria": INCOMPLETE_INCLUSION,
            },
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(PENDING, obj.eligible)
        self.assertEqual("PENDING", obj.display_label)

    def test_status_incomplete_if_eligible_other_than_missing_inclusion_criteria(self):
        opts = self.get_eligible_opts()
        opts.update(willing_to_participate=NOT_EVALUATED)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {"inclusion_criteria": INCOMPLETE_INCLUSION}, obj.reasons_ineligible
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(INCOMPLETE, obj.eligible)
        self.assertEqual(INCOMPLETE, obj.display_label)

    def test_status_incomplete_if_eligible_other_than_missing_exclusion_criteria(self):
        opts = self.get_eligible_opts()
        opts.update(prior_cm_episode=NOT_EVALUATED)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {"exclusion_criteria": INCOMPLETE_EXCLUSION}, obj.reasons_ineligible
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(INCOMPLETE, obj.eligible)
        self.assertEqual(INCOMPLETE, obj.display_label)

    def test_status_incomplete_if_missing_cd4_value(self):
        opts = self.get_eligible_opts()
        opts.update(cd4_value=None)
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {"inclusion_criteria": INCOMPLETE_INCLUSION},
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(INCOMPLETE, obj.eligible)
        self.assertEqual("INCOMPLETE", obj.display_label)

    def test_status_incomplete_if_missing_serum_crag_date(self):
        opts = self.get_eligible_opts()
        report_datetime = opts.get("report_datetime")
        cd4_date = report_datetime.date() - relativedelta(days=20)
        opts.update(
            cd4_date=cd4_date,
            serum_crag_date=None,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {"inclusion_criteria": INCOMPLETE_INCLUSION},
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(INCOMPLETE, obj.eligible)
        self.assertEqual("INCOMPLETE", obj.display_label)

    def test_status_incomplete_if_eligible_other_than_missing_inclusion_and_exclusion_criteria(
        self,
    ):
        opts = self.get_eligible_opts()
        opts.update(
            willing_to_participate=NOT_EVALUATED,
            prior_cm_episode=NOT_EVALUATED,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {
                "inclusion_criteria": INCOMPLETE_INCLUSION,
                "exclusion_criteria": INCOMPLETE_EXCLUSION,
            },
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(INCOMPLETE, obj.eligible)
        self.assertEqual(INCOMPLETE, obj.display_label)

    def test_status_not_incomplete_if_ineligible_and_missing_inclusion_criteria(self):
        opts = self.get_eligible_opts()
        opts.update(
            hiv_pos=NO,
            hiv_confirmed_date=None,
            hiv_confirmed_method=NOT_APPLICABLE,
            willing_to_participate=NOT_EVALUATED,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {"hiv_pos": "Not HIV sero-positive", "inclusion_criteria": INCOMPLETE_INCLUSION},
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_status_not_incomplete_if_ineligible_and_missing_exclusion_criteria(self):
        opts = self.get_eligible_opts()
        opts.update(
            prior_cm_episode=YES,
            jaundice=NOT_EVALUATED,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {
                "exclusion_criteria": INCOMPLETE_EXCLUSION,
                "prior_cm_episode": "Prior episode of CM",
            },
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)

    def test_status_not_incomplete_if_ineligible_and_missing_inclusion_and_exclusion_criteria(
        self,
    ):
        opts = self.get_eligible_opts()
        opts.update(
            hiv_pos=NOT_EVALUATED,
            hiv_confirmed_date=None,
            hiv_confirmed_method=NOT_APPLICABLE,
            willing_to_participate=NO,
            prior_cm_episode=YES,
            jaundice=NOT_EVALUATED,
        )
        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertDictEqual(
            {
                "inclusion_criteria": INCOMPLETE_INCLUSION,
                "willing_to_participate": "Unwilling to participate",
                "exclusion_criteria": INCOMPLETE_EXCLUSION,
                "prior_cm_episode": "Prior episode of CM",
            },
            obj.reasons_ineligible,
        )
        self.assertFalse(obj.is_eligible)
        self.assertEqual(NO, obj.eligible)
        self.assertEqual("INELIGIBLE", obj.display_label)
