from edc_constants.constants import (
    DEAD,
    MALIGNANCY,
    NOT_APPLICABLE,
    OTHER,
    OTHER_PLEASE_SPECIFY_TEXT,
    UNKNOWN,
)
from edc_constants.disease_constants import (
    BACTERAEMIA,
    BACTERIAL_PNEUMONIA,
    CM_IRIS,
    CRYPTOCOCCAL_MENINGITIS,
    CRYPTOCOCCAL_MENINGITIS_RELAPSE,
    SEPSIS,
    TB_PULMONARY,
)

list_data = {
    "edc_adverse_event.aeclassification": [
        (CRYPTOCOCCAL_MENINGITIS, "Cryptococcal meningitis"),
        ("anaemia", "Anaemia"),
        (BACTERAEMIA, "Bacteraemia"),
        (CRYPTOCOCCAL_MENINGITIS_RELAPSE, "Cryptococcal meningitis relapse"),
        (CM_IRIS, "CM-IRIS"),
        ("diarrhoea", "Diarrhoea"),
        ("hypokalaemia", "Hypokalaemia"),
        ("neutropaenia", "Neutropaenia"),
        ("pneumonia", "Pneumonia"),
        ("respiratory_distress", "Respiratory distress"),
        ("tb", "TB"),
        ("thrombocytopenia", "Thrombocytopenia"),
        ("renal_impairment", "Renal impairment"),
        (SEPSIS, "Sepsis"),
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
        (BACTERAEMIA, "Bacteraemia"),
        (BACTERIAL_PNEUMONIA, "Bacterial pneumonia"),
        ("covid_19", "COVID-19"),
        (CRYPTOCOCCAL_MENINGITIS_RELAPSE, "Cryptococcal meningitis relapse"),
        (CM_IRIS, "CM-IRIS"),
        ("iris_non_cm", "IRIS non-CM"),
        (TB_PULMONARY, "TB - Pulmonary"),
        ("tb_meningitis", "TB - Meningitis"),
        ("tb_disseminated", "TB - Disseminated"),
        ("art_toxicity", "ART toxicity"),
        (MALIGNANCY, "Malignancy"),
        ("diarrhea_wasting", "Diarrhea/wasting"),
        (SEPSIS, "Sepsis"),
        (UNKNOWN, "Unknown"),
        (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    ],
}
