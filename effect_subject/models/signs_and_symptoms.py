from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO_NA, YES_NO_UNKNOWN
from edc_constants.constants import NOT_APPLICABLE
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_model import models as edc_models

from effect_lists.models import SiSx

from ..constants import IF_ADMITTED_COMPLETE_REPORTS, IF_YES_COMPLETE_AE, SX_ACTION


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
        default=NOT_APPLICABLE,
    )

    current_sx = models.ManyToManyField(
        SiSx,
        related_name="sx",
        verbose_name="Is patient currently experiencing any of the following signs/symptoms?",
    )

    current_sx_other = models.TextField(
        verbose_name="If other, please specify ...",
        null=True,
        blank=True,
        help_text="If more than one, separate each with a comma (,).",
    )

    current_sx_gte_g3 = models.ManyToManyField(
        SiSx,
        related_name="sx_gte_g3",
        verbose_name="For these signs/symptoms, were any Grade 3 or above?",
        help_text=f"{IF_YES_COMPLETE_AE}</br>",
    )

    current_sx_gte_g3_other = models.TextField(
        verbose_name="If other, please specify ...",
        null=True,
        blank=True,
        help_text="If more than one, separate each with a comma (,).",
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

    cn_palsy_left_other = edc_models.OtherCharField(
        verbose_name="If other cranial nerve palsy (left), please specify ..."
    )

    cn_palsy_right_other = edc_models.OtherCharField(
        verbose_name="If other cranial nerve palsy (right), please specify ..."
    )

    focal_neurologic_deficit_other = edc_models.OtherCharField(
        verbose_name="If other focal neurologic deficit, please specify ..."
    )

    visual_field_loss = models.TextField(
        verbose_name="If visual field loss, please provide details ...",
        null=True,
        blank=True,
    )

    reportable_as_ae = models.CharField(
        verbose_name="Are any of these signs or symptoms Grade 3 or above?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=IF_YES_COMPLETE_AE,
    )

    patient_admitted = models.CharField(
        verbose_name="Has the patient been admitted due to any of these signs or symptoms?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=IF_ADMITTED_COMPLETE_REPORTS,
    )

    xray_performed = models.CharField(
        verbose_name="Was an X-ray performed?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If YES, complete 'Chest X-ray' CRF.",
    )

    lp_performed = models.CharField(
        verbose_name="Was a lumbar puncture performed?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If YES, complete 'Lumbar Puncture/CSF' CRF.",
    )

    urinary_lam_performed = models.CharField(
        verbose_name="Was a urinary LAM performed?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If YES, complete 'TB Diagnostics' CRF.",
    )

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Signs and Symptoms"
        verbose_name_plural = "Signs and Symptoms"
