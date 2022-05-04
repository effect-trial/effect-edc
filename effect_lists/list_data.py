from edc_constants.constants import (
    DEAD,
    HEADACHE,
    NONE,
    NORMAL,
    NOT_APPLICABLE,
    OTHER,
    OTHER_PLEASE_SPECIFY_TEXT,
    UNKNOWN,
    VISUAL_LOSS,
)
from edc_csf.constants import (
    CN_PALSY_LEFT_OTHER,
    CN_PALSY_RIGHT_OTHER,
    FOCAL_NEUROLOGIC_DEFICIT_OTHER,
)
from edc_ltfu.constants import LOST_TO_FOLLOWUP
from edc_offstudy.constants import LATE_EXCLUSION, OTHER_RX_DISCONTINUATION, WITHDRAWAL
from edc_transfer.constants import TRANSFERRED

list_data = {
    "effect_lists.nonadherencereasons": [
        ("forget_to_take", "I sometimes forget to take my pills"),
        ("dont_like_taking", "I don't like taking my pills"),
        ("make_me_ill", "My pills sometimes make me feel sick"),
        ("misplaced_pills", "I sometimes misplace my pills"),
        ("dont_believe_pills_help", "I don't believe my pills are helping me"),
        ("dont_believe_pills_needed", "I don't believe I need to take my pills"),
        ("not_feeling_well", "I have not been feeling well"),
        (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    ],
    "effect_lists.antibiotics": [
        ("amoxicillin", "Amoxicillin"),
        ("ampicillin", "Ampicillin"),
        ("flucloxacillin", "Flucloxacillin"),
        ("doxycycline", "Doxycycline"),
        ("ceftriaxone", "Ceftriaxone"),
        (
            "ciprofloxacin",
            "Ciprofloxacin (NB avoid on concomitant high dose fluconazole)",
        ),
        (
            "erythromycin",
            "Erythromycin (NB contra-indicated on concomitant high dose fluconazole)",
        ),
        ("gentamicin", "Gentamicin"),
        (
            OTHER,
            (
                "Other antibiotic, (NB avoid with concomitant high dose fluconazole), "
                "please specify below ..."
            ),
        ),
    ],
    "effect_lists.arvregimens": [
        (NOT_APPLICABLE, "--Not applicable"),
        ("ABC_3TC/FTC", "ABC + 3TC/FTC"),
        ("ABC_3TC_ATV_r", "ABC + 3TC + ATV/r"),
        ("ABC_3TC_DTG", "ABC + 3TC + DTG"),
        ("ABC_3TC_EFV", "ABC + 3TC + EFV"),
        ("ABC_3TC_LPV_r", "ABC + 3TC + LPV/r"),
        ("AZT_3TC_ATV_r", "AZT + 3TC + ATV/r"),
        ("AZT_3TC_DTG", "AZT + 3TC + DTG"),
        ("AZT_3TC_EFV", "AZT + 3TC + EFV"),
        ("AZT_3TC_LPV_r", "AZT + 3TC + LPV/r"),
        ("AZT_3TC_NVP", "AZT + 3TC + NVP"),
        ("AZT_FTC/3TC", "AZT + FTC/3TC"),
        ("D4T_3TC_NVP", "D4T + 3TC + NVP"),
        ("DTG_ABC/3TC_ATV_r", "DTG + (ABC/3TC) + ATV/r"),
        ("TDF_3TC_ATV_r", "TDF + 3TC + ATV/r"),
        ("TDF_3TC_DTG", "TDF + 3TC + DTG"),
        ("TDF_3TC_EFV", "TDF + 3TC + EFV"),
        ("TDF_3TC_LPV_r", "TDF + 3TC + LPV/r"),
        ("TDF_3TC_NVP", "TDF + 3TC + NVP"),
        ("TDF_FTC/3TC", "TDF + FTC/3TC"),
        ("TDF_FTC_ATV_r", "TDF + FTC + ATV/r"),
        ("TDF_FTC_DTG", "TDF + FTC + DTG"),
        ("TDF_FTC_EFV", "TDF + FTC + EFV"),
        ("TDF_FTC_LPV_r", "TDF + FTC + LPV/r"),
        ("TDF_FTC_NVP", "TDF + FTC + NVP"),
        ("ZDV_3TC_EFV", "ZDV + 3TC + EFV"),
        ("ZDV_3TC_NVP", "ZDV + 3TC + NVP"),
        ("ZDV_LPV_NVP", "ZDV + LPV + NVP"),
        ("EFV", "EFV"),
        ("NVP", "NVP"),
        ("DTG", "DTG"),
        ("ATZ_r", "ATZ/r"),
        ("DRV_r", "DRV/r"),
        ("lopinavir_r", "Lopinavir/r"),
        ("abacavir", "Abacavir"),
        (UNKNOWN, "Unknown"),
        (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    ],
    "effect_lists.bloodtests": [
        (NONE, "--No bloods taken"),
        (NOT_APPLICABLE, "--Not applicable (if no signs or symptoms related to CM)"),
        ("chemistry", "Chemistry"),
        ("hematology", "Hematology"),
        (OTHER, "Other bloods, please specify below ..."),
    ],
    "effect_lists.drugs": [
        ("k", "K"),
        ("mg", "Mg"),
        ("vitamins", "Vitamins"),
        ("anticonvulsants", "Anticonvulsants"),
        ("antimalarials", "Antimalarials"),
        (OTHER, "Other drug/intervention, please specify below ..."),
    ],
    "effect_lists.dx": [
        (NOT_APPLICABLE, "--Not applicable"),
        ("bacteraemia", "Bacteraemia"),
        ("bacterial_pneumonia", "Bacterial pneumonia"),
        ("cryptococcal_meningitis", "Cryptococcal meningitis"),
        ("diarrhoeal_wasting", "Diarrhoeal wasting"),
        ("kaposi_sarcoma", "Kaposi’s sarcoma"),
        ("malaria", "Malaria"),
        ("tb_extra_pulmonary", "TB extra-pulmonary"),
        ("tb_pulmonary", "TB pulmonary"),
        (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    ],
    "effect_lists.medication": [
        ("TMP-SMX", "TMP-SMX"),
        ("steroids", "Steroids, please specify type and dose below ..."),
        (OTHER, "Other medication, please specify below ..."),
    ],
    "effect_lists.offstudyreasons": [
        ("completed_followup", "Patient completed 12 months of follow-up"),
        ("clinical_endpoint", "Patient reached a clinical endpoint"),
        ("toxicity", "Patient experienced an unacceptable toxicity"),
        (
            "intercurrent_illness",
            "Intercurrent illness which prevents further treatment",
        ),
        (LOST_TO_FOLLOWUP, "Patient lost to follow-up"),
        (DEAD, "Patient reported/known to have died"),
        (WITHDRAWAL, "Patient withdrew consent to participate further"),
        (LATE_EXCLUSION, "Patient fulfilled late exclusion criteria*"),
        (TRANSFERRED, "Patient has been transferred to another health centre"),
        (
            OTHER_RX_DISCONTINUATION,
            "Other condition that justifies the discontinuation of "
            "treatment in the clinician’s opinion, please specify below ...",
        ),
        (
            OTHER,
            "Other reason, please specify below ...",
        ),
    ],
    "effect_lists.sisx": [
        (NONE, "--No symptoms to report"),
        (NOT_APPLICABLE, "--Not applicable (if signs or symptoms 'Unknown')"),
        ("cough", "Cough"),
        ("double_vision", "Double vision"),
        ("drowsiness", "Drowsiness"),
        ("fever", "Fever"),
        ("focal_weakness", "Focal weakness"),
        (HEADACHE, "Headache"),
        ("hearing_loss", "Hearing loss"),
        ("jaundice", "Jaundice"),
        ("nausea", "Nausea"),
        ("night_sweats", "Night sweats"),
        ("CN_VI_palsy_left", "Neuro - Cranial Nerve VI palsy (left)"),
        ("CN_VI_palsy_right", "Neuro - Cranial Nerve VI palsy (right)"),
        ("CN_VII_palsy_left", "Neuro - Cranial Nerve VII palsy (left)"),
        ("CN_VII_palsy_right", "Neuro - Cranial Nerve VII palsy (right)"),
        (
            CN_PALSY_LEFT_OTHER,
            "Neuro - Other cranial nerve palsy (left), please specify below ...",
        ),
        (
            CN_PALSY_RIGHT_OTHER,
            "Neuro - Other cranial nerve palsy (right), please specify below ...",
        ),
        ("focal_seizures_left", "Neuro - Focal seizures (left)"),
        ("focal_seizures_right", "Neuro - Focal seizures (right)"),
        ("hemiplegia_left", "Neuro - Hemiplegia (left)"),
        ("hemiplegia_right", "Neuro - Hemiplegia (right)"),
        ("meningism", "Neuro - Meningism"),
        ("papilloedema", "Neuro - Papilloedema"),
        ("visual_field_disturbance", "Neuro - Visual field disturbance"),
        (
            FOCAL_NEUROLOGIC_DEFICIT_OTHER,
            "Neuro - Other focal neurologic deficit, please specify below ...",
        ),
        ("shortness_of_breath", "Shortness of breath"),
        ("skin_lesions", "Skin lesions"),
        (VISUAL_LOSS, "Visual loss"),
        ("vomiting", "Vomiting"),
        ("weight_loss", "Weight loss"),
        (OTHER, "Other sign(s)/symptom(s), please specify below ..."),
    ],
    "effect_lists.sisxmeningitis": [
        ("double_vision", "Double vision"),
        ("drowsiness", "Drowsiness"),
        ("fever", "Fever"),
        ("focal_weakness", "Focal weakness"),
        (HEADACHE, "Headache"),
        ("hearing_loss", "Hearing loss"),
        ("nausea", "Nausea"),
        (
            CN_PALSY_LEFT_OTHER,
            "Neuro - Other cranial nerve palsy (left), please specify below ...",
        ),
        (
            CN_PALSY_RIGHT_OTHER,
            "Neuro - Other cranial nerve palsy (right), please specify below ...",
        ),
        ("focal_seizures_left", "Neuro - Focal seizures (left)"),
        ("focal_seizures_right", "Neuro - Focal seizures (right)"),
        ("hemiplegia_left", "Neuro - Hemiplegia (left)"),
        ("hemiplegia_right", "Neuro - Hemiplegia (right)"),
        ("meningism", "Neuro - Meningism"),
        ("papilloedema", "Neuro - Papilloedema"),
        ("visual_field_disturbance", "Neuro - Visual field disturbance"),
        (
            FOCAL_NEUROLOGIC_DEFICIT_OTHER,
            "Neuro - Other focal neurologic deficit, please specify below ...",
        ),
        ("shortness_of_breath", "Shortness of breath"),
        (VISUAL_LOSS, "Visual loss"),
        ("vomiting", "Vomiting"),
        ("weight_loss", "Weight loss"),
        (OTHER, "Other SSX symptomatic of meningitis ..."),
    ],
    "effect_lists.subjectvisitmissedreasons": [
        ("forgot", "Forgot / Can’t remember being told about appointment"),
        ("family_emergency", "Family emergency (e.g. funeral) and was away"),
        ("travelling", "Away travelling/visiting"),
        ("working_schooling", "Away working/schooling"),
        ("too_sick", "Too sick or weak to come to the centre"),
        ("lack_of_transport", "Transportation difficulty"),
        (
            OTHER,
            "Other reason, please specify below ...",
        ),
    ],
    "effect_lists.tbtreatments": [
        ("AM", "Am - Amikacin"),
        ("BDQ", "BDQ - Bedaquiline"),
        ("CFZ", "CFZ - Clofazimine"),
        ("DLM", "DLM - Delamanid"),
        ("E", "E - Ethambutol"),
        ("H", "H - Isoniazid"),
        ("HR", "HR - Isoniazid + Rifampicin"),
        ("HRZE", "HRZE - Isoniazid + Rifampicin + Pyrazinamide + Ethambutol"),
        ("LFX", "LFX - Levofloxacin"),
        ("LZD", "LZD - Linezolid"),
        ("MPM", "Mpm - Meropenem"),
        ("PAS", "PAS - Para-aminosalicylic acid"),
        ("PTO", "PTO - Prothionamide"),
        ("S", "S - Streptomycin"),
        ("TRD", "TRD - Terizidone"),
        ("Z", "Z - Pyrazinamide"),
        (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    ],
    "effect_lists.xrayresults": [
        (NORMAL, "Normal"),
        ("lymphadenopathy", "Lymphadenopathy"),
        ("consolidation", "Consolidation"),
        ("miliary_tb", "Miliary TB"),
        ("infiltrates", "Infiltrates"),
        (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    ],
    "edc_refusal.refusalreasons": [
        ("unwilling_to_say", "I am unwilling to say"),
        ("dont_have_time", "I don't have time"),
        ("stigma", "I am worried about stigma"),
        ("must_consult_spouse", "I need to consult my spouse"),
        ("dont_want_medication", "I don't want to take any more medication"),
        ("dont_want_to_join", "I don't want to take part"),
        ("no_clinic_time", "I don't want to spend a lot of time at the clinic"),
        ("need_to_think_about_it", "I haven't had a chance to think about it"),
        ("moving", "I am moving to another area"),
        (OTHER, "Other, please specify"),
    ],
}
