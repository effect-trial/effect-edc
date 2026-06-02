from clinicedc_constants import NO, NOT_APPLICABLE, NULL_STRING, YES
from clinicedc_constants.choices import YES_NO, YES_NO_NA, YES_NO_UNKNOWN
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel, HistoricalRecords, OtherCharField
from edc_sites.model_mixins import SiteModelMixin

from effect_lists.models import ArvRegimens

from ..choices import ARV_CHANGE_OPTIONS

YES_NO_NOT_ON_ART = (
    (YES, _(YES)),
    (NO, _(NO)),
    (NOT_APPLICABLE, _("Not applicable, not on ART at time of screening")),
)


class MyManager(models.Manager):
    use_in_migrations = True


class ArvSummary(SiteModelMixin, UniqueSubjectIdentifierFieldMixin, BaseUuidModel):
    """Data in this table was imported directly from an Excel file
    created and prepared by Kyla Murphy on 2026-05-28.

    The file was imported using
    `scripts/import_arv_summary_from_excel.py`
    """

    report_datetime = models.DateTimeField(default=timezone.now)

    at_screening = models.CharField(
        verbose_name="Was ppt on ARVs at the time of SCREENING?",
        max_length=255,
        choices=YES_NO,
        help_text="AT SCREENING, as opposed to at CrAg test or prior",
    )

    at_screening_regimen = models.ForeignKey(
        ArvRegimens,
        verbose_name="If Yes, what ARV regimen was the participant taking at screening?",
        on_delete=models.PROTECT,
        related_name="arv_summary_screening",
        null=True,
        blank=True,
        help_text="Applicable if on an ART at screening",
    )

    at_screening_regimen_other = OtherCharField()

    at_screening_regimen_start_date_known = models.CharField(
        verbose_name="Is the most recent start/restart date of this ARV regimen known?",
        max_length=255,
        choices=YES_NO_NA,
        default=NULL_STRING,
        blank=False,
    )

    at_screening_regimen_start_date = models.DateField(
        verbose_name="Most recent start/restart date of this ARV regimen?",
        null=True,
        blank=True,
    )

    cont_enrol = models.CharField(
        verbose_name="Was ART continued at enrolment?",
        max_length=255,
        choices=YES_NO_NOT_ON_ART,
    )

    cont_enrol_ever_restarted = models.CharField(
        verbose_name="If not continued at enrolment, was ART ever restarted before EoS?",
        max_length=255,
        choices=YES_NO_UNKNOWN,
        default=NULL_STRING,
        blank=False,
    )

    # if "ART not started or restarted by End of Study"
    cont_enrol_regimen_changed = models.CharField(
        verbose_name="If YES, ART continued at enrolment, was the regimen changed?",
        max_length=255,
        choices=ARV_CHANGE_OPTIONS,
        default=NULL_STRING,
        blank=False,
    )

    cont_enrol_regimen = models.ForeignKey(
        ArvRegimens,
        verbose_name="If changed, what was the new ARV regimen?",
        on_delete=models.PROTECT,
        related_name="arv_summary_at_enrol",
        null=True,
        blank=True,
        help_text="Applicable if ARV regimen changed at enrolment",
    )

    cont_enrol_regimen_other = OtherCharField()

    cont_enrol_regimen_start_date_known = models.CharField(
        verbose_name="Is the start date of this ARV regimen known?",
        max_length=255,
        choices=YES_NO_NA,
        default=NULL_STRING,
        blank=False,
    )

    cont_enrol_regimen_start_date = models.DateField(
        verbose_name="Start date of this ARV regimen",
        null=True,
        blank=True,
    )

    after_enrol_start_date = models.DateField(
        verbose_name="Most recent start/restart date of this ARV regimen",
        null=True,
        blank=True,
    )

    objects = MyManager()

    history = HistoricalRecords()

    def __str__(self):
        return self.subject_identifier

    class Meta:
        verbose_name = "Arv summary (from Excel)"
        verbose_name_plural = "Arv summaries (from Excel)"
