from edc_adverse_event.pdf_reports import AePdfReport as BaseAePdfReport
from reportlab.lib.units import cm


class AePdfReport(BaseAePdfReport):
    logo_data = {  # noqa: RUF012
        "app_label": "effect_edc",
        "filename": "effect_logo.png",
        "first_page": (4.0 * cm, 0.83 * cm),
        "later_pages": (3.0 * cm, 0.625 * cm),
    }
