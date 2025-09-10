from edc_lab import RequisitionPanel
from edc_lab_panel.constants import FBC

from .constants import BLOOD_CULTURE, CHEMISTRY, CSF_CULTURE
from .processing_profiles import (
    blood_culture_processing,
    chemistry_processing,
    csf_culture_processing,
    fbc_processing,
    tissue_biopsy_processing,
    urinalysis_processing,
)

chemistry_panel = RequisitionPanel(
    name=CHEMISTRY,
    verbose_name="Chemistry: RFT, LFT, Electrolytes",
    abbreviation="CHEM",
    processing_profile=chemistry_processing,
    utest_ids=[
        "alt",
        "creatinine",
        "albumin",
        "alp",
        "ast",
        ("crp", "C-Reactive Protein"),
        "egfr",
        "magnesium",
        "potassium",
        "sodium",
        "ggt",
        "urea",
        ("tbil", "Total Bilirubin"),
    ],
)

urinalysis_panel = RequisitionPanel(
    name="urinalysis",
    verbose_name="Urinalysis",
    abbreviation="urlys",
    processing_profile=urinalysis_processing,
    utest_ids=[
        ("proteinuria", "Proteinuria"),
    ],
)
csf_culture_panel = RequisitionPanel(
    name=CSF_CULTURE,
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
    ],
)

histopathology_panel = RequisitionPanel(
    name="tissue_biopsy",
    verbose_name="Histopathology: Tissue biopsy",
    abbreviation="TBY",
    processing_profile=tissue_biopsy_processing,
    utest_ids=[],
)

blood_culture_panel = RequisitionPanel(
    name=BLOOD_CULTURE,
    verbose_name="Blood culture",
    abbreviation="BLE",
    processing_profile=blood_culture_processing,
    utest_ids=[],
)

# TODO: update fbc_panel
fbc_panel = RequisitionPanel(
    name=FBC,
    verbose_name="Full Blood Count",
    processing_profile=fbc_processing,
    abbreviation="FBC",
    utest_ids=[
        ("haemoglobin", "Haemoglobin"),
        "wbc",
        ("platelets", "Platelets"),
        ("neutrophil", "Neutrophil absolute count"),
        ("neutrophil_diff", "Neutrophils differential count"),
        ("lymphocyte", "Lymphocyte absolute count"),
        ("lymphocyte_diff", "Lymphocyte differential count"),
    ],
)
