reporting_fieldset_tuple = (
    "Reporting",
    {"fields": ("reportable_as_ae", "patient_admitted")},
)

adherence_counselling_fieldset_tuple = (
    "Adherence counselling",
    {"fields": ("adherence_counselling", "adherence_counselling_reason_no")},
)

adherence_counselling_baseline_fieldset_tuple = (
    adherence_counselling_fieldset_tuple[0],
    {
        "fields": (
            adherence_counselling_fieldset_tuple[1]["fields"]
            + ("diary_issued", "diary_issued_reason_no")
        )
    },
)

missed_doses_fieldset_tuple = (
    "Missed doses",
    {
        "fields": (
            "flucon_doses_missed",
            "flucon_doses_missed_number",
            "flucyt_doses_missed",
            "flucyt_doses_missed_number",
        )
    },
)

medication_diary_review_fieldset_tuple = (
    "Medication reconciliation and adherence diary review",
    {
        "fields": (
            "medication_reconciliation",
            "medication_reconciliation_reason_no",
            "diary_returned",
            "diary_returned_reason_no",
            "diary_match_medication",
            "diary_match_medication_reason_no",
        )
    },
)

adherence_narrative_fieldset_tuple = (
    "Adherence narrative",
    {"fields": ("adherence_narrative",)},
)

adherence_summary_fieldset_tuple = (
    "Adherence summary",
    {
        "fields": (
            "linked_local_clinic",
            "linked_local_clinic_reason_no",
            "on_flucon",
            "on_flucon_reason_no",
            "on_arv",
            "on_arv_reason_no",
            "opinion_flucon_adherent",
            "opinion_arv_adherent",
            "adherence_narrative",
        )
    },
)
