from edc_lab import RequisitionPanel

from .processing_profiles import (
    blood_culture_processing,
    chemistry_processing,
    csf_culture_processing,
    fbc_processing,
    tissue_biopsy_processing,
)

chemistry_panel = RequisitionPanel(
    name="chemistry",
    verbose_name="Chemistry: RFT, LFT",
    abbreviation="CHEM",
    processing_profile=chemistry_processing,
    utest_ids=[
        "albumin",
        "alp",
        "alt",
        "amylase",
        "ast",
        "creatinine",
        "egfr",
        "ggt",
        "urea",
        "uric_acid",
    ],
)


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
    name="blood_culture",
    verbose_name="Blood culture",
    abbreviation="BLE",
    processing_profile=blood_culture_processing,
    utest_ids=[],
)

fbc_panel = RequisitionPanel(
    name="fbc",
    verbose_name="Full Blood Count",
    processing_profile=fbc_processing,
    abbreviation="FBC",
    utest_ids=[
        ("haemoglobin", "Haemoglobin"),
        "rbc",
        "wbc",
        "platelets",
    ],
)
