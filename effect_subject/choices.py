from edc_appointment.constants import TODAY, TOMORROW
from edc_constants.constants import (
    FREE_OF_CHARGE,
    HOSPITAL_NOTES,
    NEXT_OF_KIN,
    NO,
    NOT_APPLICABLE,
    NOT_DONE,
    OTHER,
    OTHER_PLEASE_SPECIFY_TEXT,
    OUTPATIENT_CARDS,
    PATIENT,
    PATIENT_REPRESENTATIVE,
    YES,
)
from edc_visit_tracking.constants import MISSED_VISIT, SCHEDULED, UNSCHEDULED

from .constants import (
    ART_CONTINUED,
    ART_STOPPED,
    CARING_FOR_CHILDREN,
    HOUSE_MAINTENANCE,
    INSURANCE,
    NOTHING,
    OWN_CASH,
    RELATIVE,
    STUDYING,
    WORKING,
)

ACTIVITY_CHOICES = (
    (WORKING, "Working"),
    (STUDYING, "Studying"),
    (CARING_FOR_CHILDREN, "Caring for children"),
    (HOUSE_MAINTENANCE, "House maintenance"),
    (NOTHING, "Nothing"),
    (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
)

ACTIVITY_CHOICES_NA = (
    (WORKING, "Working"),
    (STUDYING, "Studying"),
    (CARING_FOR_CHILDREN, "Caring for children"),
    (HOUSE_MAINTENANCE, "House maintenance"),
    (NOTHING, "Nothing"),
    (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    (NOT_APPLICABLE, "Not applicable"),
)

ARV_DECISION = (
    (NOT_APPLICABLE, "Not applicable"),
    (ART_CONTINUED, "ART continued"),
    (ART_STOPPED, "ART stopped"),
)

ASSESSMENT_WHO_CHOICES = (
    (PATIENT, "Participant"),
    (NEXT_OF_KIN, "Next of kin"),
    (NOT_APPLICABLE, "Not applicable (if missed)"),
    (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
)

CM_TX_CHOICES = (
    ("1w_amb_5fc", "1 week AmB + 5FC"),
    (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    (NOT_APPLICABLE, "Not applicable"),
)

ECOG_SCORES = (
    (
        "0",
        "[0] Fully active, able to carry on all pre-disease performance without restriction",
    ),
    (
        "1",
        "[1] Restricted in physically strenuous activity but "
        "ambulatory and able to carry out work of a light or sedentary nature, e.g., "
        "light house work, office work",
    ),
    (
        "2",
        "[2] Ambulatory and capable of all self-care but unable to carry out "
        "any work activities; up and about more than 50% of waking hours ",
    ),
    (
        "3",
        "[3] Capable of only limited self-care; confined to bed or chair more than "
        "50% of waking hours",
    ),
    (
        "4",
        "[4] Completely disabled; cannot carry on any self-care; "
        "totally confined to bed or chair",
    ),
    ("5", "[5] Deceased"),
)

EDUCATIONAL_ATTAINMENT_CHOICES = (
    ("no_schooling_completed", "No schooling completed"),
    ("nursery_to_8th_grade", "Nursery school to 8th grade"),
    ("some_high_school_no_diploma", "Some high school, no diploma"),
    (
        "high_school_grad_diploma_or_equiv",
        "High school graduate, diploma or the equivalent (for example: GED)",
    ),
    ("some_college_no_degree", "Some college credit, no degree"),
    ("trade_technical_vocational_training", "Trade/technical/vocational training"),
    ("associate_degree", "Associate degree"),
    ("bachelors_degree", "Bachelor's degree"),
    ("masters_degree", "Master's degree"),
    ("professional_degree", "Professional degree"),
    ("doctorate_degree", "Doctorate degree"),
)

FLUCONAZOLE_DOSES = (
    ("1200_mg_d", "Fluconazole, 1200 mg/d"),
    ("800_mg_d", "Fluconazole, 800 mg/d"),
    (OTHER, "Other (specify dose and reason below ...)"),
    (NOT_APPLICABLE, "Not applicable"),
)

FLUCONAZOLE_DOSES_D14 = (
    ("800_mg_d", "Fluconazole, 800 mg/d (as per protocol)"),
    (OTHER, "Other (specify dose and reason below ...)"),
    ("taken_off_study_drug", "No, taken off study drug"),
)

FLUCON_NEXT_DOSE_CHOICES = (
    (TODAY, "Today"),
    (TOMORROW, "Tomorrow"),
    (NOT_APPLICABLE, "Not applicable"),
)

FLUCYT_NEXT_DOSE_CHOICES = (
    ("0400", "at 04:00"),
    ("1000", "at 10:00"),
    ("1600", "at 16:00"),
    ("2200", "at 22:00"),
    (NOT_APPLICABLE, "Not applicable"),
)

LOST_INCOME_CHOICES = (
    (YES, "Yes"),
    (NO, "No (employed but did not lose earnings)"),
    (NOT_APPLICABLE, "Not applicable (includes not employed)"),
)

LP_REASON = (
    ("scheduled_per_protocol", "Scheduled per protocol"),
    ("clincal_deterioration", "Suspected Cryptococcal meningitis / Suspected IRIS"),
)

MEASURED_EST_CHOICES = (("measured", "Measured (weighed)"), ("estimated", "Estimated"))

MODIFIED_RANKIN_SCORE_CHOICES = (
    ("0", "[0] No symptoms"),
    (
        "1",
        (
            "[1] No significant disability. "
            "Able to carry out usual activities, despite some symptoms."
        ),
    ),
    (
        "2",
        (
            "[2] Slight disability. "
            "Able to look after own affairs without assistance, "
            "but unable to carry out all previous activities."
        ),
    ),
    ("3", "[3] Moderate disability. Requires some help, but able to walk unassisted."),
    (
        "4",
        (
            "[4] Moderately severe disability. "
            "Unable to attend to own bodily needs without assistance, "
            "and unable to walk unassisted."
        ),
    ),
    (
        "5",
        (
            "[5] Severe disability. "
            "Requires constant nursing care and attention, bedridden, incontinent."
        ),
    ),
    ("6", "[6] Dead"),
    (NOT_DONE, "Not done"),
)

NEGATIVE_TX_CHOICES = (
    ("deferred_local_clinic", "Deferred to local clinic"),
    ("contraindicated", "Contraindicated"),
    (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    (NOT_APPLICABLE, "Not applicable"),
)

PAYEE_CHOICES_ACTIVITIES = (
    (OWN_CASH, "Own cash"),
    (INSURANCE, "Insurance"),
    (RELATIVE, "Relative or others"),
    (FREE_OF_CHARGE, "Free"),
    (NOT_APPLICABLE, "Not applicable"),
)

PAYEE_CHOICES_DRUGS = (
    (OWN_CASH, "Own cash"),
    (INSURANCE, "Insurance"),
    (RELATIVE, "Relative or others paying for drugs"),
    (FREE_OF_CHARGE, "Free drugs from the pharmacy"),
    (NOT_APPLICABLE, "Not applicable"),
)

STEROID_CHOICES = (
    ("oral_prednisolone", "Oral prednisolone"),
    ("iv_dexamethasone", "IV Dexamethasone"),
    (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    (NOT_APPLICABLE, "Not applicable"),
)

TB_SITE_CHOICES = (
    ("pulmonary", "Pulmonary"),
    ("extra_pulmonary", "Extra-pulmonary"),
    ("both", "Both"),
    (NOT_APPLICABLE, "Not applicable"),
)

TB_TX_TYPES = (
    ("active_tb", "Active TB"),
    ("latent_tb", "Latent TB (HR: Isoniazid + Rifampicin)"),
    ("ipt", "IPT (Isoniazid Preventive Therapy)"),
    (NOT_APPLICABLE, "Not applicable"),
)

TIME_OFF_WORK_CHOICES = (
    (YES, "Yes"),
    (NO, "No (employed but did not take time off)"),
    (NOT_APPLICABLE, "Not applicable (includes not employed)"),
)

VISIT_INFO_SOURCE2 = (
    (PATIENT, "Participant"),
    (
        PATIENT_REPRESENTATIVE,
        "Participant representative (e.g., next of kin, relative, guardian)",
    ),
    (HOSPITAL_NOTES, "Hospital notes"),
    (OUTPATIENT_CARDS, "Outpatient cards"),
    (NOT_APPLICABLE, "Not applicable (if missed)"),
    (OTHER, "Other"),
)

VISIT_REASON = (
    (SCHEDULED, "Scheduled visit"),
    (UNSCHEDULED, "Unscheduled visit"),
    (MISSED_VISIT, "Missed visit"),
)

VISIT_UNSCHEDULED_REASON = (
    ("patient_unwell_outpatient", "Participant unwell (outpatient)"),
    ("patient_hospitalised", "Participant hospitalised"),
    ("routine_non_study", "Routine appointment (non-study)"),
    ("recurrence_symptoms", "Recurrence of symptoms"),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable"),
)
