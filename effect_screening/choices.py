from edc_constants.constants import (
    DECEASED,
    NEG,
    NO,
    NOT_APPLICABLE,
    NOT_DONE,
    NOT_EVALUATED,
    NOT_TESTED,
    OTHER,
    OTHER_PLEASE_SPECIFY_TEXT,
    PENDING,
    POS,
    YES,
)

from .constants import ACTIVE_SUBSTANCE_ADDICTION, RELOCATED, UNABLE_TO_CONTACT

CM_ON_CSF_METHODS = (
    ("india_ink", "Positive microscopy with India Ink or other method"),
    ("culture", "Positive culture"),
    (OTHER, "Other, please specify"),
    (NOT_APPLICABLE, "Not applicable"),
)

HIV_CONFIRMATION_METHODS = (
    ("site_rapid_test", "Rapid test by site"),
    ("historical_lab_result", "Historical lab result (ELISA/PCR/unsuppressed HIVVL)"),
    (
        "historical_clinical_note_rapid_test_result",
        "Historical clinical note/rapid test result",
    ),
    (NOT_APPLICABLE, "Not applicable"),
)

POS_NEG = (
    (POS, "Positive"),
    (NEG, "Negative"),
)

CSF_CRAG_RESULT_CHOICES = (
    (POS, "Positive"),
    (NEG, "Negative"),
    (PENDING, "Pending"),
    (NOT_DONE, "Not done"),
    (NOT_APPLICABLE, "Not applicable"),
)

CSF_YES_NO_PENDING_NA = (
    (YES, YES),
    (NO, NO),
    (PENDING, "Pending results"),
    (NOT_TESTED, "No further testing done"),
    (NOT_APPLICABLE, "Not applicable"),
)

PREG_YES_NO_NOT_EVALUATED_NA = (
    (YES, "Yes"),
    (NO, "No"),
    (NOT_APPLICABLE, "Not applicable: e.g. male or post-menopausal"),
    (NOT_EVALUATED, "Not evaluated"),
)

UNSUITABLE_REASONS = (
    (ACTIVE_SUBSTANCE_ADDICTION, "Active substance addiction"),
    (DECEASED, "Died prior to screening being completed"),
    (UNABLE_TO_CONTACT, "No reliable means of communicating with/ contacting/ following up"),
    (RELOCATED, "Relocated or planning to relocate within next 14 days to non-EFFECT site"),
    (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    (NOT_APPLICABLE, "Not applicable"),
)
