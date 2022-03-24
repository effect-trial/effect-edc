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
            "any_fluconazole_doses_missed",
            "fluconazole_doses_missed",
            "any_flucytosine_doses_missed",
            "flucytosine_doses_missed",
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
            "receiving_fluconazole",
            "receiving_fluconazole_reason_no",
            "receiving_arv",
            "receiving_arv_reason_no",
            "opinion_fluconazole_adherent",
            "opinion_art_adherent",
            "adherence_narrative",
        )
    },
)
