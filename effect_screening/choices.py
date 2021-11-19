from edc_constants.constants import (
    IND,
    NEG,
    NO,
    NOT_ANSWERED,
    NOT_APPLICABLE,
    NOT_DONE,
    NOT_TESTED,
    OTHER,
    PENDING,
    POS,
    YES,
)

REFUSAL_REASONS = (
    ("dont_have_time", "I don't have time"),
    ("must_consult_spouse", "I need to consult my spouse"),
    ("dont_want_blood_drawn", "I don't want to have the blood drawn"),
    ("dont_want_to_join", "I don't want to take part"),
    ("need_to_think_about_it", "I haven't had a chance to think about it"),
    (OTHER, "Other, please specify"),
)


POS_NEG_IND_NOT_ANSWERED = (
    (POS, "Positive"),
    (NEG, "Negative"),
    (IND, "Indeterminate"),
    (NOT_ANSWERED, "Not answered"),
)

POS_NEG_IND_PENDING_NA = (
    (POS, "Positive"),
    (NEG, "Negative"),
    (IND, "Indeterminate"),
    (PENDING, "Pending"),
    (NOT_APPLICABLE, "Not applicable"),
)


YES_NO_NOT_ANSWERED = (
    (YES, YES),
    (NO, NO),
    (NOT_ANSWERED, "Not answered"),
)

YES_NO_NA_NOT_ANSWERED = (
    (YES, YES),
    (NO, NO),
    (NOT_APPLICABLE, "Not applicable"),
    (NOT_ANSWERED, "Not answered"),
)

LP_NOT_DONE_YES_NO_NOT_ANSWERED_NA = (
    (YES, YES),
    (NO, NO),
    (NOT_APPLICABLE, "Not applicable, LP not done"),
    (NOT_ANSWERED, "Not answered"),
)

LP_DONE_YES_NO_NOT_ANSWERED_NA = (
    (YES, YES),
    (NO, NO),
    (NOT_APPLICABLE, "Not applicable, LP done"),
    (NOT_ANSWERED, "Not answered"),
)

CSF_YES_NO_PENDING_NA = (
    (YES, YES),
    (NO, NO),
    (PENDING, "Pending results"),
    (NOT_TESTED, "Additional testing not done"),
    (NOT_APPLICABLE, "Not applicable"),
)

PREG_YES_NO_NA_NOT_ANSWERED = (
    (YES, "Yes"),
    (NO, "No"),
    (NOT_APPLICABLE, "Not Applicable: e.g. male or post-menopausal"),
    (NOT_ANSWERED, "Not answered"),
)
