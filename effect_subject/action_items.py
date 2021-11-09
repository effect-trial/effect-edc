from edc_action_item import site_action_items
from edc_action_item.site_action_items import AlreadyRegistered
from edc_blood_results.action_items import (
    BloodResultsFbcAction,
    BloodResultsLftAction,
    BloodResultsRftAction,
)


def register_actions():
    for action_item_cls in [
        BloodResultsFbcAction,
        BloodResultsLftAction,
        BloodResultsRftAction,
    ]:
        try:
            site_action_items.register(action_item_cls)
        except AlreadyRegistered:
            pass


register_actions()
