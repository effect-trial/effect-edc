from django.db import models
from edc_model_fields.fields import OtherCharField

from ...choices import DAYS_MISSED, REASON_DRUG_MISSED
from . import Adherence


class MissedDosesModelMixin(models.Model):
    adherence = models.ForeignKey(Adherence, on_delete=models.PROTECT)

    day_missed = models.IntegerField(verbose_name="Day missed:", choices=DAYS_MISSED)

    missed_reason = models.CharField(
        verbose_name="Reason:", max_length=25, blank=True, choices=REASON_DRUG_MISSED
    )

    missed_reason_other = OtherCharField()

    class Meta:
        abstract = True
