from edc_crf.model_mixins import CrfInlineModelMixin
from edc_model import models as edc_models
from edc_model.models import HistoricalRecords
from edc_sites.managers import CurrentSiteManager

from .missed_doses_manager import MissedDosesManager
from .missed_doses_model_mixin import MissedDosesModelMixin


class FluconMissedDoses(MissedDosesModelMixin, CrfInlineModelMixin, edc_models.BaseUuidModel):
    objects = MissedDosesManager()
    on_site = CurrentSiteManager()
    history = HistoricalRecords()

    def natural_key(self):
        return (self.day_missed,) + self.adherence.natural_key()

    natural_key.dependencies = ["effect_subject.adherence"]

    class Meta(CrfInlineModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        crf_inline_parent = "adherence"
        verbose_name = "Fluconazole Missed Dose"
        verbose_name_plural = "Fluconazole Missed Doses"
        unique_together = ("adherence", "day_missed")
