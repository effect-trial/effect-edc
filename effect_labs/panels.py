from edc_lab import RequisitionPanel

from .processing_profiles import csf_culture_processing

csf_culture_panel = RequisitionPanel(
    name="csf_culture",
    verbose_name="CSF culture",
    abbreviation="CSFC",
    processing_profile=csf_culture_processing,
    utest_ids=[
        ("csf_wbc", "CSF WBC cell count"),
        ("lymphocyte", "Differential lymphocyte count"),
        ("neutrophil", "Differential neutrophil count"),
        ("csf_glucose", "CSF glucose"),
        ("csf_protein", "CSF protein"),
        ("csf_crag", "CSF CrAg"),
        ("csf_crag_lfa", "CSF CrAg LFA"),
        ("csf_crag_immy_lfa", "CSF CrAg IMMY LFA"),
    ],
)
