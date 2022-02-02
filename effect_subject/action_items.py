from typing import List

from edc_action_item import Action, site_action_items
from edc_action_item.site_action_items import AlreadyRegistered
from edc_adverse_event.constants import AE_INITIAL_ACTION
from edc_blood_results.action_items import (
    BloodResultsFbcAction,
    BloodResultsLftAction,
    BloodResultsRftAction,
)
from edc_constants.constants import HIGH_PRIORITY, YES
from edc_visit_schedule.utils import is_baseline

from effect_screening.models import SubjectScreening

from .constants import LP_ACTION, SX_ACTION


class SubjectVisitAction(Action):
    name = "actions_at_baseline"
    display_name = "Baseline actions"
    reference_model = "effect_subject.subjectvisit"

    priority = HIGH_PRIORITY
    show_on_dashboard = True
    create_by_user = False

    def reopen_action_item_on_change(self):
        return False

    def get_next_actions(self):
        # TODO: based on Q12 on screening form (lp_done)
        next_actions = []
        if is_baseline(self.reference_obj):
            subject_screening = SubjectScreening.objects.get(
                subject_identifier=self.subject_identifier
            )
            if subject_screening.lp_done == YES:
                next_actions = [LP_ACTION]
        return next_actions


class LpAction(Action):
    name = LP_ACTION
    display_name = "LP Result"
    reference_model = "effect_subject.lpresult"

    priority = HIGH_PRIORITY
    show_on_dashboard = True
    create_by_user = False


class SxAction(Action):
    name = SX_ACTION
    display_name = "Signs and Symptoms"
    reference_model = "effect_subject.signsandsymptoms"

    priority = HIGH_PRIORITY
    show_on_dashboard = True
    create_by_user = False

    def get_next_actions(self) -> List[str]:
        next_actions = []
        if (
            self.reference_obj.reportable_as_ae == YES
            or self.reference_obj.patient_admitted == YES
        ):
            next_actions = [AE_INITIAL_ACTION]
        return next_actions


# TODO:
# class FollowupAction(Action):
#     name = FOLLOWUP_ACTION
#     display_name = "Follow up action"
#     reference_model = "effect_subject.followup"
#
#     priority = HIGH_PRIORITY
#     show_on_dashboard = True
#     create_by_user = False
#
#     def get_next_actions(self) -> List[str]:
#         next_actions = []
#         if followup == YES:
#             next_actions = [HE_ACTION]
#         return next_actions


def register_actions():
    for action_item_cls in [
        BloodResultsFbcAction,
        BloodResultsLftAction,
        BloodResultsRftAction,
        # LpAction,
    ]:
        try:
            site_action_items.register(action_item_cls)
        except AlreadyRegistered:
            pass


register_actions()
