from edc_consent.constants import CONSENT_WITHDRAWAL
from edc_constants.constants import NOT_APPLICABLE, OTHER

from effect_prn.constants import CARE_TRANSFERRED_OUT, LATE_EXCLUSION_OTHER

ACTION_REQUIRED = (
    ("remain_on_study", "Participant to remain on trial"),
    ("to_be_withdrawn", "Participant to be withdrawn from trial"),
    (
        "remain_on_study_modified",
        "Patient remains on study but data analysis will be modified",
    ),
)

LOSS_CHOICES = (
    ("unknown_address", "Changed to an unknown address"),
    ("never_returned", "Did not return despite reminders"),
    ("bad_contact_details", "Inaccurate contact details"),
    (OTHER, "Other"),
)

PROTOCOL_VIOLATION = (
    ("failure_to_obtain_informed_consent", "Failure to obtain informed " "consent"),
    ("enrollment_of_ineligible_patient", "Enrollment of ineligible patient"),
    (
        "screening_procedure not done",
        "Screening procedure required by " "protocol not done",
    ),
    (
        "screening_or_on-study_procedure",
        "Screening or on-study procedure/lab " "work required not done",
    ),
    (
        "incorrect_research_treatment",
        "Incorrect research treatment given to " "patient",
    ),
    (
        "procedure_not_completed",
        "On-study procedure required by protocol not " "completed",
    ),
    ("visit_non-compliance", "Visit non-compliance"),
    ("medication_stopped_early", "Medication stopped early"),
    ("medication_noncompliance", "Medication_noncompliance"),
    (
        "national_regulations_not_met",
        "Standard WPD, ICH-GCP, local/national " "regulations not met",
    ),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable"),
)

STUDY_TERMINATION_REASONS = (
    ("completed_6m_followup", "Completed 6 month follow-up"),
    (CONSENT_WITHDRAWAL, "Withdrawal of consent"),
    ("consent_withdrawal", "Withdrawal of consent"),
    (
        "late_exclusion_positive_baseline_crag",
        "Late Exclusion—positive baseline CSF Crag result",
    ),
    (LATE_EXCLUSION_OTHER, "Late exclusion—Other reason"),
    ("late_exclusion_other", "Late exclusion—Other reason"),
    (
        CARE_TRANSFERRED_OUT,
        "Care transferred to another institution",
    ),
    ("patient_lost_followup", "Patient Lost to follow up"),
    ("patient_died", "Patient died"),
    (OTHER, "Other"),
)
