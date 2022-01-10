import pdb
from pprint import pprint

from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_constants.constants import FEMALE, MALE, NEG, NO, NOT_APPLICABLE, POS, YES
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
            "unsuitable_for_study": NO,
            "unsuitable_agreed": NOT_APPLICABLE,
        }

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

    def get_basic_opts(self):
        return {
            "screening_consent": YES,
            "willing_to_participate": YES,
            "consent_ability": YES,
            "report_datetime": get_utcnow(),
            "initials": "EW",
            "gender": FEMALE,
            "age_in_years": 25,
        }

    @property
    def inclusion_criteria(self):
        return dict(
            hiv_pos=YES,
            cd4_value=99,
            cd4_date=(get_utcnow() - relativedelta(months=3)).date(),
            pregnant_or_bf=NOT_APPLICABLE,
            serum_crag_value=POS,
            lp_done=YES,
            csf_crag_value=NEG,
        )

    @property
    def exclusion_criteria(self):
        return dict(
            prior_cm_epidose=NO,
            # prior_cm_epidose_date=(get_utcnow() - relativedelta(months=3)).date(),
            reaction_to_study_drugs=NO,
            on_fluconazole=NO,
            contraindicated_meds=NO,
            meningitis_symptoms=NO,
            jaundice=NO,
            csf_crag_value=NEG,
        )

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
        self.assertFalse(obj.eligible)
        self.assertNotIn("inclusion_criteria", obj.reasons_ineligible)

    def test_exclusion_criteria_for_eligibility(self):
        instance = SubjectScreening.objects.create(
            **self.exclusion_criteria, **self.get_basic_opts()
        )
        obj = ScreeningEligibility(instance)
        self.assertFalse(obj.eligible)
        self.assertNotIn("exclusion_criteria", obj.reasons_ineligible)

    def test_criteria_for_eligibility(self):
        instance = SubjectScreening.objects.create(
            self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        obj = ScreeningEligibility(instance)
        self.assertDictEqual({}, obj.reasons_ineligible)
        self.assertTrue(obj.eligible)

    def test_male_preg_raises(self):
        opts = dict(
            self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        opts.update(gender=MALE, pregnant_or_bf=YES)
        self.assertRaises(
            ScreeningEligibilityError, SubjectScreening.objects.create, **opts
        )
        opts.update(gender=FEMALE, pregnant_or_bf=NOT_APPLICABLE)
        try:
            SubjectScreening(SubjectScreening.objects.create, **opts)
        except ScreeningEligibilityError:
            self.fail("ScreeningEligibilityError unexpectedly raised")

    def test_crags_and_lp(self):
        opts = dict(
            self.inclusion_criteria,
            **self.exclusion_criteria,
            **self.get_basic_opts(),
        )
        opts.update(
            # TODO: Is this ok?  Was: lp_status=PENDING
            lp_done=YES,
        )
        instance = SubjectScreening.objects.create(**opts)
        obj = ScreeningEligibility(instance)
        self.assertFalse(obj.eligible)
        self.assertIn("exclusion_criteria", obj.reasons_ineligible)
