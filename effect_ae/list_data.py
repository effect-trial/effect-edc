from edc_constants.constants import (
    DEAD,
    MALIGNANCY,
    NOT_APPLICABLE,
    OTHER,
    OTHER_PLEASE_SPECIFY_TEXT,
    UNKNOWN,
)

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
        ("cm", "Cryptococcal meningitis"),
        ("bacteraemia", "Bacteraemia"),
        ("bacterial_pneumonia", "Bacterial pneumonia"),
        ("covid_19", "COVID-19"),
        (
            "iris_cm_relapse",
            "Cryptococcal meningitis relapse/IRIS",
        ),
        ("iris_non_cm", "IRIS non-CM"),
        ("tb_pulmonary", "TB - Pulmonary"),
        ("tb_meningitis", "TB - Meningitis"),
        ("tb_disseminated", "TB - Disseminated"),
        ("art_toxicity", "ART toxicity"),
        (MALIGNANCY, "Malignancy"),
        ("diarrhea_wasting", "Diarrhea/wasting"),
        ("sepsis", "Sepsis"),
        (UNKNOWN, "Unknown"),
        (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    ],
}
