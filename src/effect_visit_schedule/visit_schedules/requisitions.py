from edc_lab_panel.panels import sputum_panel
from edc_visit_schedule.visit import Requisition, RequisitionCollection

from effect_labs.panels import (
    blood_culture_panel,
    chemistry_panel,
    csf_culture_panel,
    fbc_panel,
    histopathology_panel,
)
from effect_visit_schedule.constants import DAY01, DAY14

requisitions_prn = RequisitionCollection(
    Requisition(show_order=150, panel=blood_culture_panel, required=True, additional=False),
    Requisition(show_order=175, panel=histopathology_panel, required=True, additional=False),
    Requisition(show_order=190, panel=csf_culture_panel, required=True, additional=False),
    Requisition(show_order=200, panel=sputum_panel, required=True, additional=False),
    Requisition(show_order=230, panel=chemistry_panel, required=True, additional=False),
    Requisition(show_order=250, panel=fbc_panel, required=True, additional=False),
    name="requisitions_prn",
)

requisitions_unscheduled = RequisitionCollection(
    name="requisitions_unscheduled",
)

requisitions_d01 = RequisitionCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=230, panel=chemistry_panel, required=True, additional=False),
    name=DAY01,
)

requisitions_d14 = RequisitionCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    name=DAY14,
)
