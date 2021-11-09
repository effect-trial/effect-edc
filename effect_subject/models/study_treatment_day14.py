from django.db import models
from edc_model import models as edc_models

from effect_lists.models import Antibiotics, Drugs, MedicinesDay14

from ..model_mixins import CrfModelMixin


class StudyTreatmentDay14(CrfModelMixin, edc_models.BaseUuidModel):

    # Treatment at day 14
    # TODO: Following section only available on day 14
    other_antibiotics_first_2w = models.ManyToManyField(
        Antibiotics,
        verbose_name="Other antibiotics given during the first 14 days?",
        related_name="antibiotics_2w",
        blank=True,
    )
    other_antibiotics_first_2w_other = edc_models.OtherCharField()

    other_drugs_first_2w = models.ManyToManyField(
        Drugs,
        verbose_name="Other drugs/intervention given during the first 14 days?",
        blank=True,
    )

    other_drugs_first_2w_other = edc_models.OtherCharField()

    prescribed_d14 = models.ManyToManyField(
        MedicinesDay14,
        verbose_name="Medicines prescribed on day 14?",
        blank=True,
    )
    medicines_rx_d14_other = edc_models.OtherCharField()

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Study Treatment: Day 14"
        verbose_name_plural = "Study Treatment: Day 14"
