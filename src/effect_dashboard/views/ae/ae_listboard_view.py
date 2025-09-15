from edc_adverse_event.view_mixins import AeListboardViewMixin

from effect_ae.pdf_reports import AePdfReport


class AeListboardView(AeListboardViewMixin):
    pdf_report_cls = AePdfReport
