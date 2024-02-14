from edc_adverse_event.model_mixins import AeInitialModelMixin
from edc_model.models import BaseUuidModel

from ...pdf_reports import AePdfReport
from .ae_effect_model_mixin import AeEffectModelMixin


class AeInitial(AeInitialModelMixin, AeEffectModelMixin, BaseUuidModel):
    pdf_report_cls = AePdfReport

    class Meta(AeInitialModelMixin.Meta, BaseUuidModel.Meta):
        pass
