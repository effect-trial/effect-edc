from edc_constants.constants import (
    IND,
    NEG,
    NO,
    NOT_APPLICABLE,
    NOT_TESTED,
    OTHER,
    PENDING,
    POS,
    YES,
)

CM_ON_CSF_METHODS = (
    ("india_ink", "Positive microscopy with India Ink"),
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
REFUSAL_REASONS = (
    ("dont_have_time", "I don't have time"),
    ("must_consult_spouse", "I need to consult my spouse"),
    ("dont_want_blood_drawn", "I don't want to have the blood drawn"),
    ("dont_want_to_join", "I don't want to take part"),
    ("need_to_think_about_it", "I haven't had a chance to think about it"),
    (OTHER, "Other, please specify"),
)

POS_NEG = (
    (POS, "Positive"),
    (NEG, "Negative"),
)

POS_NEG_PENDING_NA = (
    (POS, "Positive"),
    (NEG, "Negative"),
    (PENDING, "Pending"),
    (NOT_APPLICABLE, "Not applicable"),
)

POS_NEG_IND_PENDING_NA = (
    (POS, "Positive"),
    (NEG, "Negative"),
    (IND, "Indeterminate"),
    (PENDING, "Pending"),
    (NOT_APPLICABLE, "Not applicable"),
)

CSF_YES_NO_PENDING_NA = (
    (YES, YES),
    (NO, NO),
    (PENDING, "Pending results"),
    (NOT_TESTED, "Additional testing not done"),
    (NOT_APPLICABLE, "Not applicable"),
)

PREG_YES_NO_NA = (
    (YES, "Yes"),
    (NO, "No"),
    (NOT_APPLICABLE, "Not Applicable: e.g. male or post-menopausal"),
)
