from edc_adverse_event.pdf_reports import DeathPdfReport as BaseDeathReport
from reportlab.lib.units import cm


class DeathPdfReport(BaseDeathReport):
    logo_data = {
        "app_label": "effect_edc",
        "filename": "effect_logo.png",
        "first_page": (4.0 * cm, 0.83 * cm),
        "later_pages": (3.0 * cm, 0.625 * cm),
    }
