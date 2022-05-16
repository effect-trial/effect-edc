from django.contrib import admin

adherence_counselling_radio_fields = {"adherence_counselling": admin.VERTICAL}

adherence_counselling_baseline_radio_fields = adherence_counselling_radio_fields | {
    "diary_issued": admin.VERTICAL
}

missed_doses_radio_fields = {
    "flucon_doses_missed": admin.VERTICAL,
    "flucyt_doses_missed": admin.VERTICAL,
}

pill_count_diary_review_radio_fields = {
    "diary_match_medication": admin.VERTICAL,
    "diary_returned": admin.VERTICAL,
    "medication_reconciliation": admin.VERTICAL,
}

adherence_summary_radio_fields = {
    "linked_local_clinic": admin.VERTICAL,
    "on_arv": admin.VERTICAL,
    "on_flucon": admin.VERTICAL,
    "opinion_arv_adherent": admin.VERTICAL,
    "opinion_flucon_adherent": admin.VERTICAL,
}
