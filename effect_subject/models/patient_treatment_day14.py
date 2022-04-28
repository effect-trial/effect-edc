from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_model import models as edc_models

from effect_lists.models import Antibiotics, Drugs

from ..model_mixins import CrfModelMixin


class PatientTreatmentDay14(CrfModelMixin, edc_models.BaseUuidModel):

    # Treatment at day 14
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

    fcon_rx_d14 = models.IntegerField(
        verbose_name="Fluconazole prescribed on day 14?",
        validators=[MinValueValidator(0), MaxValueValidator(1200)],
        help_text="in mg/d. If taken off study drug, enter 0.",
    )

    fcon_rx_d14_reason = edc_models.OtherCharField(
        verbose_name="If fluconazole dose not 800 mg/d (as per protocol), specify reason ..."
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Patient Treatment: Day 14"
        verbose_name_plural = "Patient Treatment: Day 14"
