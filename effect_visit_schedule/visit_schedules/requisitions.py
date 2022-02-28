from edc_lab_panel.panels import fbc_panel, lft_panel, rft_panel, sputum_panel
from edc_visit_schedule import FormsCollection, Requisition

from effect_labs.lab_profiles import blood_culture_panel, histopathology_panel
from effect_labs.panels import csf_culture_panel
from effect_visit_schedule.constants import DAY01, DAY14

requisitions_prn = FormsCollection(
    Requisition(
        show_order=150, panel=blood_culture_panel, required=True, additional=False
    ),
    Requisition(
        show_order=175, panel=histopathology_panel, required=True, additional=False
    ),
    Requisition(
        show_order=190, panel=csf_culture_panel, required=True, additional=False
    ),
    Requisition(show_order=200, panel=sputum_panel, required=True, additional=False),
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
    Requisition(
        show_order=150, panel=blood_culture_panel, required=True, additional=False
    ),
    Requisition(
        show_order=175, panel=histopathology_panel, required=True, additional=False
    ),
    Requisition(
        show_order=190, panel=csf_culture_panel, required=True, additional=False
    ),
    Requisition(show_order=200, panel=sputum_panel, required=True, additional=False),
    name=DAY01,
)

requisitions_d14 = FormsCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    name=DAY14,
)
