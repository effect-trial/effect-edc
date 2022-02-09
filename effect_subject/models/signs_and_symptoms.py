from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO_NA, YES_NO_UNKNOWN
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_model import models as edc_models

from effect_lists.models import SiSx

from ..constants import IF_YES_COMPLETE_AE, IF_YES_COMPLETE_SAE, SX_ACTION


class SignsAndSymptoms(CrfWithActionModelMixin, edc_models.BaseUuidModel):
    action_name = SX_ACTION

    tracking_identifier_prefix = "SX"

    action_identifier = models.CharField(max_length=50, unique=True, null=True)

    tracking_identifier = models.CharField(max_length=30, unique=True, null=True)

    any_sx = models.CharField(
        verbose_name=(
            "Are there any signs or symptoms to report, since last contact with trial team?"
        ),
        max_length=15,
        choices=YES_NO_UNKNOWN,
    )

    cm_sx = models.CharField(
        verbose_name=(
            "Are any of the signs or symptoms related to cryptococcal meningitis (CM)?"
        ),
        max_length=15,
        choices=YES_NO_NA,
    )

    # Current Signs/Symptoms - Other CRF (p2)
    # Current Signs/Symptoms CRF (p2)
    current_sx = models.ManyToManyField(
        SiSx,
        related_name="sx",
        verbose_name="Is patient currently experiencing any of the following signs/symptoms?",
    )

    current_sx_other = models.TextField(
        verbose_name="If 'Other sign(s)/symptom(s)' selected, please specify ...",
        null=True,
        blank=True,
    )

    current_sx_gte_g3 = models.ManyToManyField(
        SiSx,
        related_name="sx_gte_g3",
        verbose_name="For these signs/symptoms, were any Grade 3 or above?",
        help_text=IF_YES_COMPLETE_AE,
    )

    current_sx_gte_g3_other = models.TextField(
        verbose_name=(
            "If 'Other sign(s)/symptom(s)' at Grade 3 or above selected, please specify ..."
        ),
        null=True,
        blank=True,
    )

    headache_duration = edc_models.DurationDHField(
        verbose_name=(
            "If patient currently has headache, for what duration have they had it for"
        ),
        help_text="In days and/or hours.  Note: 1 day equivalent to 24 hours.</br>",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )

    # TODO: Add/convert to calculated field
    headache_duration_microseconds = models.DurationField(
        null=True,
        blank=True,
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
        choices=YES_NO_NA,
        help_text=IF_YES_COMPLETE_AE,
    )

    patient_admitted = models.CharField(
        verbose_name="Has the patient been admitted due to any of these signs or symptoms?",
        max_length=15,
        choices=YES_NO_NA,
        help_text=IF_YES_COMPLETE_SAE,
    )

    cm_sx_lp_done = models.CharField(
        verbose_name="If the patient has CM signs or symptoms, was an LP done?",
        max_length=15,
        # TODO: if yes, LP request and LP result
        choices=YES_NO_NA,
        help_text="If yes, ...",
    )

    cm_sx_bloods_taken = models.CharField(
        verbose_name="If the patient has CM signs or symptoms, were bloods taken?",
        max_length=15,
        # TODO: if yes, chemistry/haemo
        choices=YES_NO_NA,
        help_text="If yes, ...",
    )

    cm_sx_patient_admitted = models.CharField(
        verbose_name="If the patient has CM signs or symptoms, was the patient admitted?",
        max_length=15,
        choices=YES_NO_NA,
        help_text=IF_YES_COMPLETE_SAE,
    )

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Signs and Symptoms"
        verbose_name_plural = "Signs and Symptoms"
