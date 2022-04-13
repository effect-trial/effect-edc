from django.core.validators import MinValueValidator
from django.db import models
from edc_model import models as edc_models

from effect_lists.models import Antibiotics, Drugs

from ..choices import FLUCONAZOLE_DOSES_D14
from ..model_mixins import CrfModelMixin


class PatientTreatmentDay14(CrfModelMixin, edc_models.BaseUuidModel):

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

    fluconazole_rx_d14 = models.CharField(
        verbose_name="Fluconazole prescribed on day 14?",
        max_length=25,
        choices=FLUCONAZOLE_DOSES_D14,
        help_text="in mg/d",
    )
    # TODO: Validate _other if fluconazole_rx_d14 == OTHER
    fluconazole_rx_d14_other = models.IntegerField(
        verbose_name="Other Fluconazole dose prescribed:",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
        help_text="in mg/d",
    )
    # TODO: Validate _other_reason if fluconazole_rx_d14 == OTHER
    fluconazole_rx_d14_other_reason = edc_models.OtherCharField(
        verbose_name="Other Fluconazole dose reason:"
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Patient Treatment: Day 14"
        verbose_name_plural = "Patient Treatment: Day 14"
