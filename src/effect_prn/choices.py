from clinicedc_constants import NOT_APPLICABLE, OTHER

from .constants import REMAIN_ON_STUDY_MODIFIED

LOSS_CHOICES = (
    ("unknown_address", "Changed to an unknown address"),
    ("never_returned", "Did not return despite reminders"),
    ("bad_contact_details", "Inaccurate contact details"),
    (OTHER, "Other"),
)

PROTOCOL_VIOLATION = (
    ("failure_to_obtain_informed_consent", "Failure to obtain informed consent"),
    ("enrollment_of_ineligible_patient", "Enrollment of ineligible patient"),
    (
        "screening_procedure not done",
        "Screening procedure required by protocol not done",
    ),
    (
        "screening_or_on-study_procedure",
        "Screening or on-study procedure/lab work required not done",
    ),
    (
        "incorrect_research_treatment",
        "Incorrect research treatment given to patient",
    ),
    (
        "procedure_not_completed",
        "On-study procedure required by protocol not completed",
    ),
    ("visit_non-compliance", "Visit non-compliance"),
    ("medication_stopped_early", "Medication stopped early"),
    ("medication_noncompliance", "Medication_noncompliance"),
    (
        "national_regulations_not_met",
        "Standard WPD, ICH-GCP, local/national regulations not met",
    ),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable"),
)

ACTION_REQUIRED = (
    ("remain_on_study", "Participant to remain on trial"),
    ("to_be_withdrawn", "Participant to be withdrawn from trial"),
    (
        REMAIN_ON_STUDY_MODIFIED,
        "Patient remains on study but data analysis will be modified",
    ),
)

ACTION_REQUIRED_FOLLOWUP = (
    (
        "MISSED_GT_2D_INDUCTION_RX",
        "Missed >2 days INDUCTION Rx (>2 doses FLU and/or >8 doses 5FC)",
    ),
    ("MISSED_GT_14D_CONSOLIDATION_RX", "Missed >14 days CONSOLIDATION Rx (800mg fluconazole)"),
    ("MISSED_GT_14D_MAINTENANCE_RX", "Missed >14 days MAINTENANCE Rx (200mg fluconazole)"),
    ("ENROLLED_IN_ERROR", "Ppt enrolled in error"),
    (NOT_APPLICABLE, "Not applicable"),
)
REASON_STUDY_TERMINATED = ()
