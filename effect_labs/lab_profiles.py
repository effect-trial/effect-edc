from django.conf import settings
from edc_lab import LabProfile
from edc_lab_panel.panels import sputum_panel

from .panels import (
    blood_culture_panel,
    chemistry_panel,
    csf_culture_panel,
    fbc_panel,
    histopathology_panel,
    urinalysis_panel,
)

subject_lab_profile = LabProfile(
    name="subject_lab_profile",
    requisition_model=settings.SUBJECT_REQUISITION_MODEL,
    reference_range_collection_name="effect",
)

subject_lab_profile.add_panel(fbc_panel)
subject_lab_profile.add_panel(histopathology_panel)
subject_lab_profile.add_panel(blood_culture_panel)
subject_lab_profile.add_panel(chemistry_panel)
subject_lab_profile.add_panel(sputum_panel)
subject_lab_profile.add_panel(csf_culture_panel)
subject_lab_profile.add_panel(urinalysis_panel)
