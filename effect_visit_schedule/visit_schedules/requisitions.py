from edc_lab_panel.panels import (
    blood_glucose_panel,
    fbc_panel,
    hba1c_panel,
    insulin_panel,
    lft_panel,
    lipids_panel,
    rft_panel,
)
from edc_visit_schedule import FormsCollection, Requisition
from edc_visit_schedule.constants import (
    DAY1,
    MONTH3,
    MONTH6,
    MONTH12,
    MONTH18,
    MONTH24,
    MONTH30,
    MONTH36,
)

requisitions_prn = FormsCollection(
    Requisition(
        show_order=200, panel=blood_glucose_panel, required=True, additional=False
    ),
    Requisition(show_order=220, panel=hba1c_panel, required=True, additional=False),
    Requisition(show_order=230, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=240, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=250, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=260, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=270, panel=insulin_panel, required=True, additional=False),
    name="requisitions_prn",
)

requisitions_unscheduled = FormsCollection(
    Requisition(
        show_order=200, panel=blood_glucose_panel, required=True, additional=False
    ),
    name="requisitions_unscheduled",
)

requisitions_d1 = FormsCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=40, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=60, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=70, panel=hba1c_panel, required=True, additional=False),
    name=DAY1,
)


requisitions_3m = FormsCollection(
    Requisition(show_order=40, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lft_panel, required=True, additional=False),
    name=MONTH3,
)

requisitions_6m = FormsCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=40, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lft_panel, required=True, additional=False),
    name=MONTH6,
)

requisitions_12m = FormsCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=40, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=60, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=70, panel=hba1c_panel, required=True, additional=False),
    name=MONTH12,
)

requisitions_18m = FormsCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    name=MONTH18,
)

requisitions_24m = FormsCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=40, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=60, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=70, panel=hba1c_panel, required=True, additional=False),
    name=MONTH24,
)

requisitions_30m = FormsCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=40, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lft_panel, required=True, additional=False),
    name=MONTH30,
)


requisitions_36m = FormsCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=40, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=60, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=70, panel=hba1c_panel, required=True, additional=False),
    name=MONTH36,
)
