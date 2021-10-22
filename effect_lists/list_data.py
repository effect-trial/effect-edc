from edc_constants.constants import DEAD, OTHER, UNKNOWN
from edc_ltfu.constants import LOST_TO_FOLLOWUP
from edc_offstudy.constants import LATE_EXCLUSION, OTHER_RX_DISCONTINUATION, WITHDRAWAL
from edc_transfer.constants import TRANSFERRED

from .constants import OTHER_PLEASE_SPECIFY_TEXT

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
        # TODO: ???One or two separate options?
        ("amoxicillin_ampicillin", "Amoxicillin/Ampicillin"),
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
        (OTHER, "Other  please specify below ..."),
    ],
    "effect_lists.arvregimens": [
        ("TDF_FTC_3TC", "TDF + FTC/3TC"),
        ("AZT_FTC_3TC", "AZT + FTC/3TC"),
        ("EFV", "EFV"),
        ("NVP", "NVP"),
        ("DTG", "DTG"),
        ("ATZ_r", "ATZ/r"),
        ("DRV_r", "DRV/r"),
        ("abacavir", "Abacavir"),
        ("lopinavir_r ", "Lopinavir/r"),
        (UNKNOWN, "Unknown"),
        (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    ],
    "effect_lists.drugs": [
        ("k", "K"),
        ("mg", "Mg"),
        ("vitamins", "Vitamins"),
        ("tmp_smx_cotrimoxazole", "TMP-SMX/Cotrimoxazole"),
        ("anticonvulsants", "Anticonvulsants"),
        ("antimalarials", "Antimalarials"),
        (OTHER, "Other drug/intervention, please specify below ..."),
    ],
    "effect_lists.significantnewdiagnoses": [
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
    "effect_lists.medicinesrxday14": [
        ("fluconazole_800mg", "Fluconazole (800mg as per protocol)"),
        # TODO: ???Is 'Other' a different dose of fluconazole, or a different drug?
        (
            "fluconazole_other",
            "Fluconazole (other dose), please specify dose and reason below...",
        ),
    ],
    # TODO: ???Refactor to focalneurologicdeficits (remove meningism, papilloedema)?
    "effect_lists.neurologicalconditions": [
        ("meningism", "Meningism"),
        ("papilloedema", "Papilloedema"),
        ("CN_VI_palsy_left", "Cranial Nerve VI palsy (left)"),
        ("CN_VI_palsy_right", "Cranial Nerve VI palsy (right)"),
        ("CN_VII_palsy_left", "Cranial Nerve VII palsy (left)"),
        ("CN_VII_palsy_right", "Cranial Nerve VII palsy (right)"),
        (
            "CN_palsy_left_other",
            "Other cranial nerve palsy (left), please specify below ...",
        ),
        (
            "CN_palsy_right_other",
            "Other cranial nerve palsy (right), please specify below ...",
        ),
        ("hemiplegia_left", "Hemiplegia (left)"),
        ("hemiplegia_right", "Hemiplegia (right)"),
        ("focal_seizures_left", "Focal seizures (left)"),
        ("focal_seizures_right", "Focal seizures (right)"),
        ("visual_field_disturbance", "Visual field disturbance"),
        (OTHER, "Other neurological, please specify below ..."),
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
    "effect_lists.symptoms": [
        ("headache", "Headache"),
        ("double_vision", "Double vision"),
        ("visual_loss", "Visual loss"),
        ("fever", "Fever"),
        ("hearing_loss", "Hearing loss"),
        ("drowsiness", "Drowsiness"),
        ("focal_weakness", "focal_weakness"),
        ("nausea", "Nausea"),
        ("vomiting", "Vomiting"),
        ("weight_loss", "Weight loss"),
        ("skin_lesions", "Skin lesions"),
        ("cough", "Cough"),
        ("shortness_of_breath", "Shortness of breath"),
        ("jaundice", "Jaundice"),
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
        ("HRZE", "HRZE"),
        ("HR", "HR"),
        ("E", "E"),
        ("Z", "Z"),
        ("H", "H"),
        ("BDQ", "BDQ"),
        ("PTO", "PTO"),
        ("PAS", "PAS"),
        ("LFX", "LFX"),
        ("CFZ", "CFZ"),
        ("MPM", "Mpm"),
        ("AM", "Am"),
        ("DLM", "DLM"),
        ("TRD", "TRD"),
        ("S", "S"),
        ("LZD", "LZD"),
        (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    ],
    "effect_lists.xrayresults": [
        ("lymphadenopathy", "Lymphadenopathy"),
        ("consolidation", "consolidation"),
        ("military TB", "military TB"),
        ("Infiltrates", "Infiltrates"),
        (OTHER, OTHER_PLEASE_SPECIFY_TEXT),
    ],
}
