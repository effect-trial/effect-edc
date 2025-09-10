from django.db import models
from edc_crf.model_mixins import CrfModelMixin
from edc_model import models as edc_models
from edc_visit_tracking.model_mixins import SubjectVisitMissedModelMixin

from effect_lists.models import SubjectVisitMissedReasons


class SubjectVisitMissed(
    CrfModelMixin,
    SubjectVisitMissedModelMixin,
    edc_models.BaseUuidModel,
):
    missed_reasons = models.ManyToManyField(
        SubjectVisitMissedReasons, blank=True, related_name="effect_missed_reasons"
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Missed Visit Report"
        verbose_name_plural = "Missed Visit Report"
