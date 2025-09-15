from django.db import models
from edc_crf.model_mixins import CrfInlineModelMixin
from edc_model import models as edc_models
from edc_model.models import HistoricalRecords
from edc_sites.managers import CurrentSiteManager

from ...choices import DOSES_MISSED
from .missed_doses_manager import MissedDosesManager
from .missed_doses_model_mixin import MissedDosesModelMixin


class FlucytMissedDoses(MissedDosesModelMixin, CrfInlineModelMixin, edc_models.BaseUuidModel):
    doses_missed = models.IntegerField(verbose_name="Doses missed:", choices=DOSES_MISSED)

    objects = MissedDosesManager()
    on_site = CurrentSiteManager()
    history = HistoricalRecords()

    def natural_key(self):
        return self.day_missed, *self.adherence.natural_key()

    natural_key.dependencies = ("effect_subject.adherence",)

    class Meta(CrfInlineModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        crf_inline_parent = "adherence"
        verbose_name = "Flucytosine Missed Dose"
        verbose_name_plural = "Flucytosine Missed Doses"
        unique_together = ("adherence", "day_missed")
