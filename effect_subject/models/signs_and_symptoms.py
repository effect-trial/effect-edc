from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_UNKNOWN
from edc_model import models as edc_models

from effect_lists.models import SiSx

from ..model_mixins import CrfModelMixin


class SignsAndSymptoms(CrfModelMixin, edc_models.BaseUuidModel):

    cm_signs_symptoms = models.CharField(
        verbose_name=(
            "Has the patient had signs or symptoms of "
            "cryptococcal meningitis (CM) since last contact with trial team?"
        ),
        max_length=15,
        choices=YES_NO_UNKNOWN,
    )

    # Current Signs/Symptoms - Other CRF (p2)
    # Current Signs/Symptoms CRF (p2)
    signs_and_symptoms = models.ManyToManyField(
        SiSx,
        verbose_name="Is patient currently experiencing any of the following signs/symptoms?",
        blank=True,
    )

    headache_duration = models.IntegerField(
        # TODO: Only valid if headache selected in current_symptoms
        verbose_name=(
            "If patient currently has headache, for what duration have they had it for"
        ),
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="in days",
    )

    visual_field_loss = models.TextField(
        # TODO: ???Link to visual_field_disturbance focal_neurologic_deficits field?
        verbose_name="If visual field loss, please provide details ...",
        null=True,
        blank=True,
    )

    reportable_as_ae = models.CharField(
        verbose_name="Are any of these signs or symptoms Grade 3 or above?",
        max_length=15,
        # TODO: If yes, prompt for SAE
        choices=YES_NO,
    )

    patient_admitted = models.CharField(
        verbose_name="Has the patient been admitted due to any of these signs or symptoms?",
        max_length=15,
        # TODO: If yes, prompt for SAE form
        choices=YES_NO,
        help_text="If yes, complete SAE report",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Signs and Symptoms"
        verbose_name_plural = "Signs and Symptoms"
