from edc_adverse_event.pdf_reports import AePdfReport
from edc_adverse_event.view_mixins import AeListboardViewMixin
from reportlab.lib.units import cm


class CustomAeReport(AePdfReport):
    logo_data = {
        "app_label": "effect_edc",
        "filename": "effect_logo.png",
        "first_page": (4.0 * cm, 0.83 * cm),
        "later_pages": (3.0 * cm, 0.625 * cm),
    }


class AeListboardView(AeListboardViewMixin):
    pdf_report_cls = CustomAeReport
