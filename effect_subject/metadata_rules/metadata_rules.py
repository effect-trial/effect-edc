from edc_constants.constants import YES
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.metadata_rules import CrfRule, CrfRuleGroup, P, register

from .predicates import Predicates

pc = Predicates()


@register()
class SignsAndSymptomsRuleGroup(CrfRuleGroup):
    chest_xray = CrfRule(
        predicate=P("xray_performed", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["chestxray"],
    )

    lp_csf = CrfRule(
        predicate=pc.lpcsf_crf_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["lpcsf"],
    )

    tb_diagnostics = CrfRule(
        predicate=P("urinary_lam_performed", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["tbdiagnostics"],
    )

    class Meta:
        app_label = "effect_subject"
        source_model = "effect_subject.signsandsymptoms"


@register()
class SubjectVisitRuleGroup(CrfRuleGroup):
    vitalsigns = CrfRule(
        predicate=pc.vitalsigns_crf_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["vitalsigns"],
    )

    class Meta:
        app_label = "effect_subject"
        source_model = "effect_subject.subjectvisit"
