from edc_constants.constants import (
    ABSENT,
    DEAD,
    MICROSCOPY,
    NO,
    NO_EXAM,
    NORMAL,
    NOT_APPLICABLE,
    NOT_DONE,
    OTHER,
    OTHER_PLEASE_SPECIFY_TEXT,
    PRESENT,
    RAPID_TEST,
    YES,
)
from edc_reportable.constants import GRADE3, GRADE4
from edc_visit_tracking.constants import MISSED_VISIT, SCHEDULED, UNSCHEDULED

from .constants import (
    APPT,
    APPT_OTHER,
    DECREASED,
    IN_PERSON,
    PATIENT,
    PRESENT_WITH_REINFORCEMENT,
    REDUCED,
    TELEPHONE,
)

ACTIVITY_CHOICES = (
    ("working", "Working"),
    ("studying", "Studying"),
    ("caring_for_children", "Caring for children"),
    (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
)

ANKLE_REFLEX_CHOICES = (
    (PRESENT, "Present"),
    (PRESENT_WITH_REINFORCEMENT, "Present/Reinforcement"),
    (ABSENT, "Absent"),
    (NOT_APPLICABLE, "Not applicable"),
)

ANTIBIOTIC_CHOICES = (
    ("amoxicillin", "Amoxicillin"),
    ("ceftriaxone", "Ceftriaxone"),
    ("ciprofloxacin", "Ciprofloxacin"),
    ("doxycycline", "Doxycycline"),
    ("erythromycin", "Erythromycin (contraindicated with high dose fluconazole)"),
    ("flucloxacillin", "Flucloxacillin"),
    (
        OTHER,
        "Other (avoid with concomitant high dose fluconazole), please specify below ...",
    ),
)

ASSESSMENT_TYPES = ((TELEPHONE, "Telephone"), (IN_PERSON, "In person"))

CHILDCARE_CHOICES = (
    (NOT_APPLICABLE, "Not applicable"),
    ("working", "Working"),
    ("studying", "Studying"),
    ("caring_for_children", "Caring for children"),
    ("house_maintenance", "House maintenance"),
    ("nothing", "Nothing"),
    (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
)

CM_TX_CHOICES = (
    ("1w_amb_5fc", "1 week AmB + 5FC"),
    (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    (NOT_APPLICABLE, "Not applicable (no CM treatment given)"),
)

DYSLIPIDAEMIA_RX_CHOICES = (
    ("atorvastatin", "Atorvastatin"),
    ("rosuvastatin", "Rosuvastatin"),
    (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    (NOT_APPLICABLE, "Not applicable"),
)

ECOG_SCORES = (
    (
        "0",
        "Fully active, able to carry on all pre-disease performance without restriction",
    ),
    (
        "1",
        "Restricted in physically strenuous activity but "
        "ambulatory and able to carry out work of a light or sedentary nature, e.g., "
        "light house work, office work",
    ),
    (
        "2",
        "Ambulatory and capable of all self-care but unable to carry out "
        "any work activities; up and about more than 50% of waking hours ",
    ),
    (
        "3",
        "Capable of only limited self-care; confined to bed or chair more than "
        "50% of waking hours",
    ),
    (
        "4",
        "Completely disabled; cannot carry on any self-care; totally confined to bed or chair",
    ),
    ("5", "Deceased"),
)

FOLLOWUP_REASONS = (
    (APPT, "Study appointment"),
    (APPT_OTHER, "Other routine appointment"),
    (UNSCHEDULED, "Unschedule visit"),
    (OTHER, "Other reason, specify below ..."),
)

GRADE34_CHOICES = (
    (GRADE3, "Grade 3"),
    (GRADE4, "Grade 4"),
    (NOT_APPLICABLE, "Not applicable"),
)

INFO_SOURCE = (
    ("hospital_notes", "Hospital notes"),
    ("outpatient_cards", "Outpatient cards"),
    ("patient", "Patient"),
    ("collateral_history", "Collateral History from relative/guardian"),
    (NOT_APPLICABLE, "Not applicable (if missed)"),
    (OTHER, "Other"),
)


FUNDOSCOPY_CHOICES = (
    ("no_retinopathy", "No retinopathy"),
    ("background_retinopathy", "Background retinopathy"),
    ("pre_proliferative_retinopathy", "Pre-proliferative retinopathy"),
    ("proliferative_retinopathy", "Proliferative retinopathy"),
    ("maculopathy", "Maculopathy"),
    (NO_EXAM, "Exam not performed"),
)

MALARIA_TEST_CHOICES = (
    (RAPID_TEST, "Rapid test"),
    (MICROSCOPY, "Microscopy"),
    (NOT_APPLICABLE, "Not applicable"),
)

MEASURED_EST_CHOICES = (("measured", "Measured (weighed)"), ("estimated", "Estimated"))

MODIFIED_RANKIN_SCORE_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    (NOT_DONE, "Not done"),
)

MONOFILAMENT_CHOICES = (
    (NORMAL, "Normal"),
    (REDUCED, "Reduced"),
    (ABSENT, "Absent"),
    (NOT_APPLICABLE, "Not applicable"),
)

PAYEE_CHOICES = (
    ("own_cash", "Own cash"),
    ("insurance", "Insurance"),
    ("relative", "Relative of others paying"),
    ("free", "Free drugs from the pharmacy"),
    (NOT_APPLICABLE, "Not applicable"),
)

PRESENT_ABSENT_NOEXAM = (
    (PRESENT, "Present"),
    (ABSENT, "Absent"),
    (NO_EXAM, "Exam not performed"),
)

PRESENT_ABSENT_NOEXAM_NDS = (
    (PRESENT, "Present"),
    (PRESENT_WITH_REINFORCEMENT, "Present with reinforcement"),
    (ABSENT, "Absent"),
    (NO_EXAM, "Exam not performed"),
)
# 0 = Present   1 = Present with reinforcement   2 = Absent

PATIENT_STATUSES = (
    ("alive_well", "Alive and well"),
    ("alive_unwell", "Alive, but unwell"),
    (DEAD, "Deceased"),
)

INFO_SOURCES = (
    (PATIENT, "Patient"),
    ("next_of_kin", "Next of kin"),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable (in person visit)"),
)

STEROID_CHOICES = (
    ("oral_prednisolone", "Oral prednisolone"),
    ("iv_dexamethasone", "IV Dexamethasone"),
    (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    (NOT_APPLICABLE, "Not applicable (no steroids administered)"),
)

TRANSPORT_CHOICES = (
    ("bus", "Bus"),
    ("train", "Train"),
    ("ambulance", "Ambulance"),
    ("private_taxi", "Private taxi"),
    ("own_bicycle", "Own bicycle"),
    ("hired_motorbike", "Hired motorbike"),
    ("own_car", "Own car"),
    ("own_motorbike", "Own motorbike"),
    ("hired_bicycle", "Hired bicycle"),
    ("foot", "Foot"),
    (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
)

ULCERATION_CHOICES = (
    (ABSENT, "Absent"),
    (PRESENT, "Present"),
    (NOT_APPLICABLE, "Not applicable"),
)

VIBRATION_PERCEPTION_CHOICES = (
    (PRESENT, "Present"),
    (DECREASED, "Decreased"),
    (ABSENT, "Absent"),
    (NOT_APPLICABLE, "Not applicable"),
)

VISIT_UNSCHEDULED_REASON = (
    ("patient_unwell_outpatient", "Patient unwell (outpatient)"),
    ("patient_hospitalised", "Patient hospitalised"),
    ("routine_non_study", "Routine appointment (non-study)"),
    ("recurrence_symptoms", "Recurrence of symptoms"),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable"),
)

VISIT_REASON = (
    (SCHEDULED, "Scheduled visit"),
    (UNSCHEDULED, "Unscheduled visit"),
    (MISSED_VISIT, "Missed visit"),
)

WEIGHT_DETERMINATION = (("estimated", "Estimated"), ("measured", "Measured"))

YES_NO_NO_EXAM = (
    (YES, YES),
    (NO, NO),
    (NO_EXAM, "Exam not performed"),
)
