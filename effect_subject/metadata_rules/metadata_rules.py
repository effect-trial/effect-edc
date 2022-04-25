from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.metadata_rules import CrfRule, CrfRuleGroup, P, register

from .predicates import Predicates

pc = Predicates()


@register()
class SignsAndSymptomsRuleGroup(CrfRuleGroup):

    chest_xray = CrfRule(
        predicate=pc.chest_xray_crf_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["chestxray"],
    )

    lp_csf = CrfRule(
        predicate=pc.lp_csf_crf_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["lpcsf"],
    )

    tb_diagnostics = CrfRule(
        predicate=pc.tb_diagnostics_crf_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["tbdiagnostics"],
    )

    class Meta:
        app_label = "effect_subject"
        source_model = "effect_subject.signsandsymptoms"
