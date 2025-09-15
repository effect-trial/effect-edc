from edc_adverse_event.view_mixins import DeathReportListboardViewMixin

from effect_ae.pdf_reports import DeathPdfReport


class DeathReportListboardView(DeathReportListboardViewMixin):
    pdf_report_cls = DeathPdfReport
