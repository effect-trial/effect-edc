from edc_constants.constants import (
    DEAD,
    MALIGNANCY,
    NOT_APPLICABLE,
    OTHER,
    OTHER_PLEASE_SPECIFY_TEXT,
    UNKNOWN,
)
from edc_constants.disease_constants import (
    BACTERAEMIA_SEPSIS,
    BACTERIAL_PNEUMONIA,
    CM_RELAPSE_IRIS,
    COVID_19,
    CRYPTOCOCCAL_MENINGITIS,
    TB_PULMONARY,
)

list_data = {
    "edc_adverse_event.aeclassification": [
        (CRYPTOCOCCAL_MENINGITIS, "Cryptococcal meningitis"),
        ("anaemia", "Anaemia"),
        (BACTERAEMIA_SEPSIS, "Bacteraemia/sepsis"),
        (CM_RELAPSE_IRIS, "Cryptococcal meningitis relapse/IRIS"),
        ("diarrhoea", "Diarrhoea"),
        ("hypokalaemia", "Hypokalaemia"),
        ("neutropaenia", "Neutropaenia"),
        ("pneumonia", "Pneumonia"),
        ("respiratory_distress", "Respiratory distress"),
        ("tb", "TB"),
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
        (CRYPTOCOCCAL_MENINGITIS, "Cryptococcal meningitis"),
        (BACTERAEMIA_SEPSIS, "Bacteraemia/sepsis"),
        (BACTERIAL_PNEUMONIA, "Bacterial pneumonia"),
        (COVID_19, "COVID-19"),
        (CM_RELAPSE_IRIS, "Cryptococcal meningitis relapse/IRIS"),
        ("iris_non_cm", "IRIS non-CM"),
        (TB_PULMONARY, "TB - Pulmonary"),
        ("tb_meningitis", "TB - Meningitis"),
        ("tb_disseminated", "TB - Disseminated"),
        ("art_toxicity", "ART toxicity"),
        (MALIGNANCY, "Malignancy"),
        ("diarrhea_wasting", "Diarrhea/wasting"),
        ("pcp", "PCP"),
        ("toxoplasmosis", "Toxoplasmosis"),
        (UNKNOWN, "Unknown"),
        (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    ],
}
