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
            "any_doses_missed",
            "fluconazole_doses_missed",
            "flucytosine_doses_missed",
        )
    },
)

pill_count_diary_review_fieldset_tuple = (
    "Pill count and adherence diary review",
    {
        "fields": (
            "pill_count_conducted",
            "pill_count_conducted_reason_no",
            "diary_returned",
            "diary_returned_reason_no",
            "diary_match_pill_count",
            "diary_match_pill_count_reason_no",
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
            "opinion_fluconazole_adherent",
            "opinion_art_adherent",
            "adherence_narrative",
        )
    },
)
