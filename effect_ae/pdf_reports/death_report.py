from edc_adverse_event.pdf_reports import DeathPdfReport as BaseDeathReport

from .pdf_report_mixin import CrfReportMixin


class DeathReport(CrfReportMixin, BaseDeathReport):
    pass
