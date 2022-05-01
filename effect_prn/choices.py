from edc_constants.constants import NOT_APPLICABLE, OTHER

LOSS_CHOICES = (
    ("bad_contact_details", "Inaccurate contact details"),
    ("never_returned", "Did not return despite reminders"),
    ("unknown_address", "Changed to an unknown address"),
    (OTHER, "Other"),
)

PROTOCOL_VIOLATION = (
    ("failure_obtain_informed_consent", "Failure to obtain informed " "consent"),
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
    ("visit_non_compliance", "Visit non-compliance"),
    ("medication_stopped_early", "Medication stopped early"),
    ("medication_noncompliance", "Medication_noncompliance"),
    (
        "national_regulations_not_met",
        "Standard WPD, ICH-GCP, local/national " "regulations not met",
    ),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable"),
)

ACTION_REQUIRED = (
    ("remain_on_study", "Participant to remain on trial"),
    (
        "remain_on_study_modified",
        "Patient remains on study but data analysis will be modified",
    ),
    ("to_be_withdrawn", "Participant to be withdrawn from trial"),
)

MEDICINES = (
    ("co_trimaxazole", "Co-trimaxazole"),
    ("fluconazole_200mg", "Fluconazole (200mg)"),
    ("rifampicin", "Rifampicin"),
    (OTHER, "Other"),
)

FLUCONAZOLE_DOSE_14DAYS = (
    ("800", "800"),
    ("1200", "1200"),
    (OTHER, "Other"),
)

FLUCONAZOLE_DOSE_CONSOLIDATION = (
    ("200", "200"),
    (OTHER, "Other"),
)

STUDY_TERMINATION_REASONS = (
    (
        "care_transferred_out",
        "Care transferred to another institution",
    ),
    ("completed_6month_followup", "Completed 6 month follow-up"),
    ("consent_withdrawal", "Withdrawal of consent"),
    ("late_exclusion_other_reason", "Late exclusion—Other reason"),
    (
        "late_exclusion_positive_baseline_crAg",
        "Late Exclusion—positive baseline CSF CrAg result",
    ),
    ("patient_died", "Patient died"),
    ("patient_lost_followup", "Patient Lost to follow up"),
    (OTHER, "Other"),
)

REASON_STUDY_TERMINATED = ()
