from clinicedc_constants.choices import YES_NO, YES_NO_NA
from django.db import models
from django.utils import timezone
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin

from effect_lists.models import ArvRegimens

from ..choices import ARV_CHANGE_OPTIONS


class ArvSummary(SiteModelMixin, UniqueSubjectIdentifierFieldMixin, BaseUuidModel):
    report_datetime = models.DateTimeField(default=timezone.now)

    # does this imply adherence??
    at_screening = models.CharField(
        verbose_name="Was ppt on ARVs at the time of SCREENING?",
        max_length=255,
        choices=YES_NO,
        help_text="AT SCREENING, as opposed to at CrAg test or prior",
    )

    at_screening_regimen = models.ForeignKey(
        ArvRegimens,
        verbose_name=("If Yes, what ARV regimen was the participant taking at screening?"),
        on_delete=models.PROTECT,
        related_name="arv_summary_screening",
        null=True,
        blank=True,
        help_text="Applicable if on an ART at screening",
    )

    at_screening_start_date_known = models.CharField(
        verbose_name="Is the most recent start/restart date of this ARV regimen known?",
        max_length=255,
        choices=YES_NO_NA,
    )

    at_screening_start_date = models.DateField(
        verbose_name="Most recent start/restart date of this ARV regimen?",
        null=True,
        blank=True,
    )

    cont_enrol = models.CharField(
        verbose_name="Were ARVs continued AT enrolment?",
        max_length=255,
        choices=YES_NO_NA,
    )

    cont_enrol_changed = models.CharField(
        verbose_name="Were ARVs changed AT enrolment?",
        max_length=255,
        choices=ARV_CHANGE_OPTIONS,
    )

    cont_enrol_regimen = models.ForeignKey(
        ArvRegimens,
        verbose_name="What ARV regimen was the participant taking at enrolment?",
        on_delete=models.PROTECT,
        related_name="arv_summary_at_enrol",
        null=True,
        blank=True,
        help_text="Applicable if ARV regimen changed at enrolment",
    )

    after_enrol = models.CharField(
        verbose_name="Were ARVs continued AFTER enrolment?",
        max_length=255,
        choices=YES_NO_NA,
    )

    after_enrol_regimen = models.ForeignKey(
        ArvRegimens,
        verbose_name="What ARV regimen did the participant continued AFTER enrolment?",
        on_delete=models.PROTECT,
        related_name="arv_summary_after_enrol",
        null=True,
        blank=True,
        help_text="Applicable if ARV regimen was continued after enrolment",
    )

    after_enrol_start_date_known = models.CharField(
        verbose_name="Is the most recent start/restart date of this ARV regimen known?",
        max_length=255,
        choices=YES_NO_NA,
    )

    after_enrol_start_date = models.DateField(
        verbose_name=("Most recent start/restart date of this ARV regimen"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Arv summary"
        verbose_name_plural = "Arv summaries"
