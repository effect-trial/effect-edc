from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_constants.constants import (
    FEMALE,
    MALE,
    NEG,
    NO,
    NOT_APPLICABLE,
    OTHER,
    PENDING,
    POS,
    YES,
)
from edc_utils.date import get_utcnow

from effect_lists.models import SiSxMeningitis
from effect_screening.eligibility import ScreeningEligibility
from effect_screening.forms import SubjectScreeningForm
from effect_screening.models import SubjectScreening
from effect_subject.constants import HEADACHE

from ..effect_test_case_mixin import EffectTestCaseMixin


class TestForms(EffectTestCaseMixin, TestCase):
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
        }

    @property
    def inclusion_criteria(self):
        return dict(
            hiv_pos=YES,
            cd4_value=99,
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
            jaundice=NO,
            mg_ssx_since_crag=NO,
            on_fluconazole=NO,
            pregnant=NOT_APPLICABLE,
            breast_feeding=NOT_APPLICABLE,
            prior_cm_epidose=NO,
            reaction_to_study_drugs=NO,
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
        form = SubjectScreeningForm(
            initial=self.get_data(), instance=SubjectScreening()
        )
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

    def test_mg_ssx(self):
        opts = dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        opts.update(mg_ssx_since_crag=YES)

        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("mg_ssx", form._errors)

        ssx = SiSxMeningitis.objects.filter(name=HEADACHE)
        opts.update(mg_ssx=ssx)

        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("mg_ssx", form._errors)

        ssx = SiSxMeningitis.objects.filter(name=OTHER)
        opts.update(mg_ssx=ssx)

        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("mg_ssx_other", form._errors)

        opts.update(mg_ssx_other="blah blah")

        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("mg_ssx_other", form._errors)
