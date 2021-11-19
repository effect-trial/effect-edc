from edc_model.models import HistoricalRecords
from edc_sites.models import CurrentSiteManager as BaseCurrentSiteManager

from .daily_closing_log import DailyClosingLog
from .utils import get_daily_log_revision_date

# TODO: how many CrAg tests results were available per week for those with CD4 < 100 above age 18.


class CurrentSiteManager(BaseCurrentSiteManager):
    def get_by_natural_key(self, log_date, site):
        return self.get(log_date=log_date, site=site)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(log_date__gte=get_daily_log_revision_date())


class DailyClosingLogRevisedManager(BaseCurrentSiteManager):
    def get_by_natural_key(self, log_date, site):
        return self.get(log_date=log_date, site=site)


class DailyClosingLogRevised(DailyClosingLog):
    """Second iteration of Daily Closing Log form."""

    on_site = CurrentSiteManager()

    objects = DailyClosingLogRevisedManager()

    history = HistoricalRecords()

    class Meta:
        proxy = True
        verbose_name = "Daily Closing Log (post-enrollment)"
        verbose_name_plural = "Daily Closing Logs (post-enrollment)"
