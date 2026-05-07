from clinicedc_constants.choices import YES_NO, YES_NO_NA
from django.db import models
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin

from effect_lists.models import ArvRegimens

from ..choices import ARV_CHANGE_OPTIONS


class ArvSummary(SiteModelMixin, UniqueSubjectIdentifierFieldMixin, BaseUuidModel):
    # does this imply adherence??
    art_at_screening = models.CharField(
        verbose_name=("Was ppt on ARVs at the time of SCREENING?"),
        max_length=255,
        choices=YES_NO,
        help_text="AT SCREENING, as opposed to at CrAg test or prior",
    )

    art_regimen_at_screening = models.ForeignKey(
        ArvRegimens,
        verbose_name="What ARV regimen was the participant taking at the time of screening?",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="Required if on an ART at screening",
    )

    art_start_date_known = models.CharField(
        verbose_name=("Is the most recent start/restart date of this ARV regimen known?"),
        max_length=255,
        choices=YES_NO_NA,
    )

    art_start_date = models.DateField(
        verbose_name="Most recent start/restart date of this ARV regimen?",
        null=True,
        blank=True,
    )

    art_cont_enrol = models.CharField(
        verbose_name=("Were ARVs continued AT enrolment?"),
        max_length=255,
        choices=YES_NO_NA,
    )

    art_changed_enrol = models.CharField(
        verbose_name=("Were ARVs changed AT enrolment?"),
        max_length=255,
        choices=ARV_CHANGE_OPTIONS,
    )

    art_after_enrol = models.CharField(
        verbose_name=("Were ARVs continued AFTER enrolment?"),
        max_length=255,
        choices=YES_NO_NA,
    )

    art_after_enrol_regimen = models.ForeignKey(
        ArvRegimens,
        verbose_name="What ARV regimen did the participant continued AFTER enrolment?",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    art_after_enrol_startdate = models.DateField(
        verbose_name=(
            "Most recent start/restart date of the ARV regimen continued AFTER enrolment?"
        ),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Arv summary"
        verbose_name_plural = "Arv summaries"
