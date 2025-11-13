from copy import deepcopy

from clinicedc_constants import PENDING
from django.test import TestCase, tag

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
            user_created="erikvw",
            user_modified="erikvw",
            **get_eligible_options(),
        )
