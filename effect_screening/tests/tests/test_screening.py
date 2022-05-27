from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_constants.constants import NO, YES
from edc_utils.date import get_utcnow_as_date

from effect_screening.eligibility import ScreeningEligibility
from effect_screening.forms import SubjectScreeningForm
from effect_screening.models import SubjectScreening

from ..effect_test_case_mixin import EffectTestCaseMixin
from . import TestEligibility


@tag("subjscr")
class TestSubjectScreening(EffectTestCaseMixin, TestCase):
    """See also `test_eligibility.py` for eligibility tests."""

    def test_screening_opts_eligible(self):
        obj = SubjectScreening.objects.create(**TestEligibility().get_valid_opts())

        elig_obj = ScreeningEligibility(model_obj=obj)
        self.assertDictEqual({}, elig_obj.reasons_ineligible)
        self.assertTrue(elig_obj.is_eligible)

    def test_screening_opts_validate_ok(self):
        form = SubjectScreeningForm(data=TestEligibility().get_valid_opts())
        form.is_valid()
        self.assertDictEqual({}, form._errors)

    def test_expected_behaviour_hiv_dx_date(self):
        opts = TestEligibility().get_valid_opts()
        opts.update(
            hiv_dx_ago=None,
            hiv_dx_date=get_utcnow_as_date() - relativedelta(days=30),
        )
        obj = SubjectScreening.objects.create(**opts)
        obj.save()
        obj.refresh_from_db()

        self.assertEqual(obj.hiv_dx_ago, None)
        self.assertEqual(
            obj.hiv_dx_date,
            get_utcnow_as_date() - relativedelta(days=30),
        )
        self.assertEqual(obj.hiv_dx_date_is_estimated, NO)
        self.assertEqual(obj.hiv_dx_estimated_date, None)
        self.assertEqual(obj.best_hiv_dx_date, obj.hiv_dx_date)

        elig_obj = ScreeningEligibility(model_obj=obj)
        self.assertDictEqual({}, elig_obj.reasons_ineligible)
        self.assertTrue(elig_obj.is_eligible)

    def test_expected_behaviour_hiv_dx_ago(self):
        opts = TestEligibility().get_valid_opts()
        opts.update(
            hiv_dx_ago="28d",
            hiv_dx_date=None,
        )
        obj = SubjectScreening.objects.create(**opts)
        obj.save()
        obj.refresh_from_db()

        self.assertEqual(obj.hiv_dx_ago, "28d")
        self.assertEqual(obj.hiv_dx_date, None)
        self.assertEqual(
            obj.hiv_dx_estimated_date,
            get_utcnow_as_date() - relativedelta(days=28),
        )
        self.assertEqual(obj.hiv_dx_date_is_estimated, YES)
        self.assertEqual(obj.best_hiv_dx_date, obj.hiv_dx_estimated_date)

        elig_obj = ScreeningEligibility(model_obj=obj)
        self.assertDictEqual({}, elig_obj.reasons_ineligible)
        self.assertTrue(elig_obj.is_eligible)
