from edc_constants.constants import (
    DECLINED,
    DONE,
    NEG,
    NOT_APPLICABLE,
    OTHER,
    PENDING,
    POS,
)

REFUSAL_REASONS = (
    ("dont_have_time", "I don't have time"),
    ("must_consult_spouse", "I need to consult my spouse"),
    ("dont_want_blood_drawn", "I don't want to have the blood drawn"),
    ("dont_want_to_join", "I don't want to take part"),
    ("need_to_think_about_it", "I haven't had a chance to think about it"),
    (OTHER, "Other, please specify"),
)

LP_STATUS = (
    (DONE, "Done"),
    (PENDING, "Done"),
    (DECLINED, "Done"),
)


CSF_RESULT = (
    (POS, "CM Positive"),
    (NEG, "CM Negative"),
    (NOT_APPLICABLE, "Not applicable"),
)
