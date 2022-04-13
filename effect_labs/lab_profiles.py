from django.conf import settings
from edc_lab import LabProfile, ProcessingProfile, RequisitionPanel
from edc_lab.aliquot_types import tissue_biopsy, wb
from edc_lab_panel.panels import (
    blood_glucose_poc_panel,
    hba1c_panel,
    lft_panel,
    lipids_panel,
    rft_panel,
    sputum_panel,
)
from edc_lab_panel.processing_profiles import fbc_processing

from .panels import csf_culture_panel

tissue_biopsy_processing = ProcessingProfile(name="TBY", aliquot_type=tissue_biopsy)
blood_culture_processing = ProcessingProfile(name="BLE", aliquot_type=wb)

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


subject_lab_profile = LabProfile(
    name="subject_lab_profile",
    requisition_model=settings.SUBJECT_REQUISITION_MODEL,
    reference_range_collection_name="effect",
)

subject_lab_profile.add_panel(blood_glucose_poc_panel)
subject_lab_profile.add_panel(fbc_panel)
subject_lab_profile.add_panel(hba1c_panel)
subject_lab_profile.add_panel(histopathology_panel)
subject_lab_profile.add_panel(blood_culture_panel)
subject_lab_profile.add_panel(lft_panel)
subject_lab_profile.add_panel(lipids_panel)
subject_lab_profile.add_panel(rft_panel)
subject_lab_profile.add_panel(sputum_panel)
subject_lab_profile.add_panel(csf_culture_panel)
