from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from effect_lists.models import FocalNeurologicDeficits

from ..model_mixins import CrfModelMixin


class Neurological(CrfModelMixin, edc_models.BaseUuidModel):

    # Current Signs/Symptoms - Neurological Questions CRF (p2)
    meningism = models.CharField(
        verbose_name="Meningism?",
        max_length=15,
        choices=YES_NO,
    )

    papilloedema = models.CharField(
        verbose_name="Papilloedema?",
        max_length=15,
        choices=YES_NO,
    )

    focal_neurologic_deficits = models.ManyToManyField(
        FocalNeurologicDeficits,
        related_name="focal_neurologic_deficits",
        verbose_name="Does patient have any of the following focal neurologic deficits?",
    )

    focal_neurologic_deficits_other = edc_models.OtherCharField(
        verbose_name="If other focal neurologic deficit, please specify ..."
    )

    cn_palsy_left_other = edc_models.OtherCharField(
        verbose_name="If other cranial nerve palsy (left), please specify ..."
    )

    cn_palsy_right_other = edc_models.OtherCharField(
        verbose_name="If other cranial nerve palsy (right), please specify ..."
    )

    reportable_as_ae = models.CharField(
        verbose_name="Are any of these neurological symptoms Grade 3 or above?",
        max_length=15,
        # TODO: If yes, prompt for SAE
        choices=YES_NO,
    )

    patient_admitted = models.CharField(
        verbose_name="Has the patient been admitted due to these neurological symptoms?",
        max_length=15,
        # TODO: If yes, prompt for SAE form
        choices=YES_NO,
        help_text="If yes, complete SAE report",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Neurological Symptoms"
        verbose_name_plural = "Neurological Symptoms"
