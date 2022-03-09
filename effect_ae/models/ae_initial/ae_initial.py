from edc_adverse_event.model_mixins import AeInitialModelMixin
from edc_model.models import BaseUuidModel

from .ae_effect_model_mixin import AeEffectModelMixin


class AeInitial(AeInitialModelMixin, AeEffectModelMixin, BaseUuidModel):
    class Meta(AeInitialModelMixin.Meta):
        pass
