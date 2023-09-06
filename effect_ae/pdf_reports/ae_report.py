from edc_adverse_event.pdf_reports import AePdfReport as BaseAeReport

from .pdf_report_mixin import CrfReportMixin


class AeReport(CrfReportMixin, BaseAeReport):
    pass
