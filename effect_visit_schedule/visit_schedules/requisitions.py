from edc_lab_panel.panels import fbc_panel, lft_panel, rft_panel
from edc_visit_schedule import FormsCollection, Requisition

from effect_visit_schedule.constants import DAY01, DAY14

requisitions_prn = FormsCollection(
    Requisition(show_order=230, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=240, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=250, panel=fbc_panel, required=True, additional=False),
    name="requisitions_prn",
)

requisitions_unscheduled = FormsCollection(
    name="requisitions_unscheduled",
)

requisitions_d01 = FormsCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    name=DAY01,
)

requisitions_d14 = FormsCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    name=DAY14,
)
