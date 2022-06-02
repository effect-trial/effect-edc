from datetime import date, datetime
from typing import Any, Union

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import SELECTION_METHOD
from edc_model.models import BaseUuidModel
from edc_model.models.historical_records import HistoricalRecords
from edc_sites.models import CurrentSiteManager as BaseCurrentSiteManager
from edc_sites.models import SiteModelMixin
from edc_utils import convert_php_dateformat, get_utcnow


def get_daily_log_revision_date() -> Union[date, datetime]:
    try:
        return settings.EFFECT_SCREENING_DCL_REVISION_DATETIME.date()
    except AttributeError:
        return settings.EFFECT_SCREENING_DCL_REVISION_DATETIME


class CurrentSiteManager(BaseCurrentSiteManager):
    def get_by_natural_key(self, log_date, site):
        return self.get(log_date=log_date, site=site)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(log_date__lt=get_daily_log_revision_date())


class DailyClosingLogManager(BaseCurrentSiteManager):
    def get_by_natural_key(self, log_date, site):
        return self.get(log_date=log_date, site=site)


class DailyClosingLog(SiteModelMixin, BaseUuidModel):

    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        null=True,
        related_name="+",
    )

    log_date = models.DateField(verbose_name="Clinic date", default=get_utcnow)

    attended = models.IntegerField(
        verbose_name="Total number of patients who attended the clinic today",
        validators=[MinValueValidator(0)],
    )

    selection_method = models.CharField(
        verbose_name="How were patients selected to be approached?",
        max_length=25,
        choices=SELECTION_METHOD,
        null=True,
    )

    approached = models.IntegerField(
        verbose_name="Of those who attended, how many were approached by the study team",
        validators=[MinValueValidator(0)],
        null=True,
    )

    agreed_to_screen = models.IntegerField(
        verbose_name="Of those approached, how many agreed to be screened",
        validators=[MinValueValidator(0)],
        null=True,
    )

    clinic_start_time = models.TimeField(
        verbose_name="Clinic start time",
        null=True,
        help_text="Use 24HRS format. For example 17:00",
    )

    clinic_end_time = models.TimeField(
        verbose_name="Clinic End time",
        null=True,
        help_text="Use 24HRS format. For example 17:00",
    )

    comment = models.TextField(
        verbose_name="Additional Comments",
        null=True,
        blank=True,
    )

    on_site = CurrentSiteManager()

    objects = DailyClosingLogManager()

    history = HistoricalRecords()

    def __str__(self):
        return self.log_date.strftime(convert_php_dateformat(settings.DATE_FORMAT))

    def natural_key(self: Any):
        return (
            self.log_date,
            self.site,
        )

    class Meta:
        verbose_name = "Daily Closing Log"
        verbose_name_plural = "Daily Closing Logs"
        constraints = [
            models.UniqueConstraint(fields=["log_date", "site"], name="unique_date_for_site"),
        ]
