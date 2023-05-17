from edc_adverse_event.constants import DISCHARGED, INPATIENT
from edc_constants.constants import DECEASED, NOT_APPLICABLE, OTHER, UNKNOWN

AE_TYPE = (
    ("sae", "Serious Adverse Event / Reaction"),
    ("aesi", "Adverse Event of Special Interest"),
    ("susar", "Serious Unexpected Adverse Reaction"),
)

AE_EXPECTED = (
    ("expected", "Expected"),
    ("unexpected", "Unexpected"),
)

AE_ACTION_REQUIRED = (
    ("action", "Further action is required"),
    ("no_action", "No further action is required"),
)

DEATH_LOCATIONS = (
    ("home", "At home"),
    ("hospital_clinic", "Hospital/clinic"),
    ("home", "Elsewhere"),
)


INFORMANT_RELATIONSHIP = (
    ("husband_wife", "Husband/wife"),
    ("Parent", "Parent"),
    ("child", "Child"),
    (UNKNOWN, "Unknown"),
    (OTHER, "Other"),
)

INPATIENT_STATUSES = (
    (INPATIENT, "Currently an inpatient"),
    (DISCHARGED, "Discharged"),
    (DECEASED, "Died during hospitalization"),
    (NOT_APPLICABLE, "Not applicable"),
)
