from edc_constants.constants import NOT_APPLICABLE, OTHER

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

ACTION_REQUIRED = (
    ("remain_on_study", "Participant to remain on trial"),
    ("to_be_withdrawn", "Participant to be withdrawn from trial"),
    (
        "remain_on_study_modified",
        "Patient remains on study but data analysis will be modified",
    ),
)

MEDICINES = (
    ("fluconazole_200mg", "Fluconazole (200mg)"),
    ("rifampicin", "Rifampicin"),
    ("co_trimaxazole", "co_trimaxazole"),
    (OTHER, "Other"),
)

DIAGNOSIS = (
    ("tuberculosis_pulmonary", "Tuberculosis pulmonary"),
    ("tuberculosis_extra_pulmonary", "Tuberculosis extra-pulmonary"),
    ("bacteraemia", "Bacteraemia"),
    ("bacterial_pneumonia", "Bacterial pneumonia"),
    ("cryptococcal_meningitis", "Cryptococcal meningitis"),
    ("kaposis_syndrome", "Kaposi’s syndrome"),
    ("diarrhoeal_wasting", "Diarrhoeal wasting"),
    ("malaria", "Malaria"),
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
    ("completed_6month_followup", "Completed 6 month follow-up"),
    ("Withdrawal of consent", "Withdrawal of consent"),
    (
        "Late Exclusion—positive baseline CSF CrAg result",
        "Late Exclusion—positive baseline CSF CrAg result",
    ),
    ("Late exclusion—Other reason", "Late exclusion—Other reason"),
    (
        "Care transferred to another institution",
        "Care transferred to another institution",
    ),
    ("Patient Lost to follow up", "Patient Lost to follow up"),
    ("Patient died", "Patient died"),
    (OTHER, "Other"),
)

REASON_STUDY_TERMINATED = ()
