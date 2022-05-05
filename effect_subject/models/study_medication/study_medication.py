from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_model import models as edc_models

from ...model_mixins import CrfModelMixin


class StudyMedication(CrfModelMixin, edc_models.BaseUuidModel):

    modifications = models.CharField(
        verbose_name=(
            "Have there been any modifications " "to study medication since the last report"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    flucon_initiated = models.CharField(
        verbose_name="Was the patient started on Fluconazole?",
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

    flucon_dose = models.IntegerField(
        verbose_name="Fluconazole dose (mg)",
        null=True,
        blank=True,
    )

    flucon_dose_datetime = models.DateTimeField(
        verbose_name="Date and time of first Fluconazole dose",
        null=True,
        blank=True,
    )

    flucon_notes = models.TextField(
        verbose_name="Fluconazole notes (if any)",
        max_length=250,
        null=True,
        blank=True,
    )

    flucyt_initiated = models.CharField(
        verbose_name="Was the patient started on Flucytosine?",
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

    flucyt_dose = models.IntegerField(
        verbose_name="Flucytosine dose (mg)",
        null=True,
        blank=True,
        help_text=(
            "Validate against weight and rando arm "
            "100mg/kg, round down to nearest 500mg total "
            "e.g. 47kg = 4700mg, patient gets 4500mg daily"
        ),
    )

    flucyt_dose_datetime = models.DateTimeField(
        verbose_name="Date and time of first Flucytosine dose",
        null=True,
        blank=True,
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
