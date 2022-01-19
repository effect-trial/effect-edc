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
from edc_screening.screening_eligibility import ScreeningEligibilityError
from edc_utils.date import get_utcnow

from effect_screening.eligibility import ScreeningEligibility
from effect_screening.forms import SubjectScreeningForm
from effect_screening.models import SubjectScreening

from ..effect_test_case_mixin import EffectTestCaseMixin


@tag("screen")
class TestForms(EffectTestCaseMixin, TestCase):
    def get_data(self):
        return {
            "screening_consent": YES,
            "willing_to_participate": YES,
            "consent_ability": YES,
            "report_datetime": get_utcnow(),
            "initials": "EW",
            "gender": MALE,
            "age_in_years": 25,
        }

    def get_basic_opts(self):
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
            # prior_cm_epidose_date=(get_utcnow() - relativedelta(months=3)).date(),
            contraindicated_meds=NO,
            csf_cm_evidence=NO,
            jaundice=NO,
            meningitis_symptoms=NO,
            on_fluconazole=NO,
            pregnant_or_bf=NOT_APPLICABLE,
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
        # self.assertEqual(form._errors, {})
        # form.save()
        # self.assertTrue(SubjectScreening.objects.all()[0].eligible)

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

    @tag("123")
    def test_male_preg_raises(self):
        opts = dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        opts.update(
            gender=MALE,
            pregnant_or_bf=YES,
            unsuitable_for_study=NO,
            unsuitable_agreed=NOT_APPLICABLE,
            lp_declined=NOT_APPLICABLE,
        )
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertIn("pregnant_or_bf", form._errors)

        opts.update(gender=FEMALE, pregnant_or_bf=NOT_APPLICABLE)
        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertDictEqual({}, form._errors)

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
        # self.assertIn("exclusion_criteria", obj.reasons_ineligible)

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

    @tag("wa")
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

    @tag("wa")
    def test_csf_cm_evidence(self):
        opts = dict(
            **self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        opts.update(csf_cm_evidence=YES)

        form = SubjectScreeningForm(data=opts)
        form.is_valid()
        self.assertNotIn("csf_cm_evidence", form._errors)

        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertIn("csf_cm_evidence", obj.reasons_ineligible)
        self.assertFalse(obj.is_eligible)

        opts.update(csf_cm_evidence=NO)

        model_obj = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(model_obj=model_obj)
        self.assertNotIn("csf_cm_evidence", obj.reasons_ineligible)
        self.assertTrue(obj.is_eligible)
