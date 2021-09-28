from edc_constants.constants import DEAD, OTHER, UNKNOWN
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
        (OTHER, "Other, please specify ..."),
    ],
    "effect_lists.arvregimens": [
        ("ABC_3TC_ATV_r", "ABC + 3TC + ATV/r"),
        ("ABC_3TC_LPV_r", "ABC + 3TC + LPV/r"),
        ("AZT_3TC_ATV_r", "AZT + 3TC + ATV/r"),
        ("AZT_3TC_EFV", "AZT + 3TC + EFV"),
        ("AZT_3TC_LPV_r", "AZT + 3TC + LPV/r"),
        ("AZT_3TC_NVP", "AZT + 3TC + NVP"),
        ("D4T_3TC_NVP", "D4T + 3TC + NVP"),
        ("DTG_ABC/3TC_ATV_r", "DTG + (ABC/3TC) + ATV/r"),
        ("TDF_3TC_ATV_r", "TDF + 3TC + ATV/r"),
        ("TDF_3TC_DTG", "TDF + 3TC + DTG"),
        ("TDF_3TC_EFV", "TDF + 3TC + EFV"),
        ("TDF_3TC_LPV_r", "TDF + 3TC + LPV/r"),
        ("TDF_FTC_ATV_r", "TDF + FTC + ATV/r"),
        ("TDF_FTC_EFV", "TDF + FTC + EFV"),
        ("TDF_FTC_LPV_r", "TDF + FTC + LPV/r"),
        ("ZDV_3TC_EFV", "ZDV + 3TC + EFV"),
        ("ZDV_3TC_NVP", "ZDV + 3TC + NVP"),
        ("ZDV_LPV_NVP", "ZDV + LPV + NVP"),
        (UNKNOWN, "Unknown"),
        (OTHER, "Other, specify ..."),
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
            "treatment in the clinician’s opinion (specify below)",
        ),
        (
            OTHER,
            "Other reason (specify below)",
        ),
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
            "Other reason (specify below)",
        ),
    ],
}
