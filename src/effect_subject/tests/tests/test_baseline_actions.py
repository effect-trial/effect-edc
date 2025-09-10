from copy import deepcopy

from django.test import TestCase, tag
from edc_constants.constants import PENDING

from effect_screening.models import SubjectScreening
from effect_screening.tests.effect_test_case_mixin import (
    EffectTestCaseMixin,
    get_eligible_options,
)


class TestBaselineActions(EffectTestCaseMixin, TestCase):
    @tag("aa")
    def test_lp_action(self):
        opts = deepcopy(get_eligible_options())
        opts.update(lp_done=PENDING)
        SubjectScreening.objects.create(
            user_created="erikvw", user_modified="erikvw", **get_eligible_options()
        )
