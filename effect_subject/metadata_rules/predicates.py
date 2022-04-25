from typing import Union

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import YES
from edc_metadata.metadata_rules import PredicateCollection


def required_if_field_response(
    model_cls,
    visit,
    field: str,
    response: Union[str, int, bool],
) -> bool:
    """Require if:
    - `model_cls` CRF exists for the `visit`, and
    - the `field` is equal to the expected `response`, and
    - answer to `field` matches `response`.
    """
    try:
        obj = model_cls.objects.get(subject_visit_id=visit.id)
    except ObjectDoesNotExist:
        required = False
    else:
        required = getattr(obj, field) == response
    return required


class Predicates(PredicateCollection):

    app_label = "effect_subject"
    visit_model = "effect_subject.subjectvisit"

    def chest_xray_crf_required(self, visit, **kwargs) -> bool:
        """Require if SiSx answer for visit to `xray_performed` is `YES`."""
        sisx_model_cls = django_apps.get_model(f"{self.app_label}.signsandsymptoms")
        return required_if_field_response(sisx_model_cls, visit, "xray_performed", YES)

    def lp_csf_crf_required(self, visit, **kwargs) -> bool:
        """Require if SiSx answer for visit to `lp_performed` is `YES`."""
        sisx_model_cls = django_apps.get_model(f"{self.app_label}.signsandsymptoms")
        return required_if_field_response(sisx_model_cls, visit, "lp_performed", YES)

    def tb_diagnostics_crf_required(self, visit, **kwargs) -> bool:
        """Require if SiSx answer for visit to `urinary_lam_performed` is `YES`."""
        sisx_model_cls = django_apps.get_model(f"{self.app_label}.signsandsymptoms")
        return required_if_field_response(
            sisx_model_cls, visit, "urinary_lam_performed", YES
        )
