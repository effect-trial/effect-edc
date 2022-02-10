from edc_constants.constants import DEAD, NOT_APPLICABLE, OTHER, UNKNOWN

list_data = {
    "edc_adverse_event.aeclassification": [
        ("cm", "Cryptococcal Meningitis"),
        ("anaemia", "Anaemia"),
        ("bacteraemia/sepsis", "Bacteraemia/Sepsis"),
        ("CM_IRIS", "CM IRIS"),
        ("diarrhoea", "Diarrhoea"),
        ("hypokalaemia", "Hypokalaemia"),
        ("neutropaenia", "Neutropaenia"),
        ("pneumonia", "Pneumonia"),
        ("respiratory_distress", "Respiratory distress"),
        ("TB", "TB"),
        ("thrombocytopenia", "Thrombocytopenia"),
        ("renal_impairment", "Renal impairment"),
        (OTHER, "Other"),
    ],
    "edc_adverse_event.saereason": [
        (NOT_APPLICABLE, "Not applicable"),
        (DEAD, "Death"),
        ("life_threatening", "Life-threatening"),
        ("significant_disability", "Significant disability"),
        ("in-patient_hospitalization", "In-patient hospitalization or prolongation"),
        (
            "medically_important_event",
            "Medically important event (e.g. Bacteraemia, "
            "recurrence of symptoms not requiring admission)",
        ),
    ],
    "edc_adverse_event.causeofdeath": [
        ("art_toxicity", "ART toxicity"),
        ("diarrhea_wasting", "Diarrhea/wasting"),
        (UNKNOWN, "Unknown"),
        (OTHER, "Other"),
    ],
}
