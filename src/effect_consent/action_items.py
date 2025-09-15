from edc_action_item.action import Action
from edc_action_item.site_action_items import site_action_items
from edc_constants.constants import HIGH_PRIORITY

from .constants import CONSENT_V2_ACTION, RECONSENT_ACTION


class ReconsentAction(Action):
    name = RECONSENT_ACTION
    display_name = "Re-consent participant"
    reference_model = "effect_consent.subjectreconsent"
    priority = HIGH_PRIORITY
    show_on_dashboard = True
    show_link_to_changelist = True
    admin_site_name = "effect_consent_admin"
    create_by_user = False
    singleton = True
    instructions = (
        "Participant must be re-consented as soon as able. "
        "Participant's ICF was initially completed by next-of-kin."
    )

    def reopen_action_item_on_change(self):
        return False


class ConsentUpdateV2Action(Action):
    name = CONSENT_V2_ACTION
    display_name = "Submit Version 2 Consent"
    reference_model = "effect_consent.subjectconsentupdatev2"
    priority = HIGH_PRIORITY
    show_on_dashboard = True
    show_link_to_changelist = True
    admin_site_name = "effect_consent_admin"
    create_by_user = False
    singleton = True
    instructions = (
        "Participant needs to complete the version 2 consent "
        "before data collection can continue."
    )

    def reopen_action_item_on_change(self):
        return False


site_action_items.register(ConsentUpdateV2Action)
site_action_items.register(ReconsentAction)
