from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models

from effect_lists.models import DoseModificationReasons

from ...choices import FLUCON_NEXT_DOSE_CHOICES, FLUCYT_NEXT_DOSE_CHOICES
from ...model_mixins import CrfModelMixin


class StudyMedication(CrfModelMixin, edc_models.BaseUuidModel):

    modifications = models.CharField(
        verbose_name=(
            "Have there been any modifications to study medication since the last report?"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    modifications_reason = models.ManyToManyField(
        DoseModificationReasons,
        verbose_name="Reason for dose change",
        blank=True,
        help_text="Select all that apply.",
    )

    modifications_reason_other = models.TextField(
        verbose_name="If other reason, please provide details ...",
        max_length=250,
        null=True,
        blank=True,
    )

    flucon_initiated = models.CharField(
        verbose_name="Was the participant started on Fluconazole?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    flucon_not_initiated_reason = models.TextField(
        verbose_name="If NO, please explain",
        max_length=250,
        null=True,
        blank=True,
    )

    flucon_modified = models.CharField(
        verbose_name=(
            "Have there been any modifications to fluconazole dose since the last report?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    flucon_dose = models.IntegerField(
        verbose_name="Fluconazole dose",
        validators=[MinValueValidator(0), MaxValueValidator(1200)],
        null=True,
        blank=True,
        help_text="in mg/d",
    )

    flucon_dose_datetime = models.DateTimeField(
        verbose_name="Date and time first fluconazole dose administered",
        null=True,
        blank=True,
    )

    flucon_next_dose = models.CharField(
        verbose_name="First fluconazole dose administered",
        max_length=15,
        choices=FLUCON_NEXT_DOSE_CHOICES,
        default=NOT_APPLICABLE,
    )

    flucon_notes = models.TextField(
        verbose_name="Fluconazole notes (if any)",
        max_length=250,
        null=True,
        blank=True,
    )

    flucyt_initiated = models.CharField(
        verbose_name="Was the participant started on Flucytosine?",
        max_length=15,
        choices=YES_NO_NA,
        null=True,
        blank=False,
    )

    flucyt_not_initiated_reason = models.TextField(
        verbose_name="If NO, please explain",
        max_length=250,
        null=True,
        blank=True,
    )

    flucyt_dose_expected = models.IntegerField(
        verbose_name="Flucytosine dose expected",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text=(
            "in mg/d. Validate against weight and rando arm "
            "100mg/kg, round down to nearest 500mg total "
            "e.g. 47kg = 4700mg, participant gets 4500mg daily"
        ),
    )

    flucyt_modified = models.CharField(
        verbose_name=(
            "Have there been any modifications to flucytosine dose since the last report?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    flucyt_dose_datetime = models.DateTimeField(
        verbose_name="Date and time first flucytosine dose administered",
        null=True,
        blank=True,
    )

    flucyt_dose = models.IntegerField(
        verbose_name="Flucytosine dose prescribed",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="in mg/d",
    )

    flucyt_dose_0400 = models.IntegerField(
        verbose_name="Dose at 04:00",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="in mg",
    )

    flucyt_dose_1000 = models.IntegerField(
        verbose_name="Dose at 10:00",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="in mg",
    )

    flucyt_dose_1600 = models.IntegerField(
        verbose_name="Dose at 16:00",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="in mg",
    )

    flucyt_dose_2200 = models.IntegerField(
        verbose_name="Dose at 22:00",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="in mg",
    )

    flucyt_next_dose = models.CharField(
        verbose_name="First flucytosine dose administered",
        max_length=5,
        choices=FLUCYT_NEXT_DOSE_CHOICES,
        default=NOT_APPLICABLE,
    )

    flucyt_notes = models.TextField(
        verbose_name="Flucytosine notes (if any)",
        max_length=250,
        null=True,
        blank=True,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Study medication"
        verbose_name_plural = "Study medication"
