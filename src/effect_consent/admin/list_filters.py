from __future__ import annotations

from django.utils.translation import gettext as _
from edc_model_admin.list_filters import PastDateListFilter


class ConsentDateListFilter(PastDateListFilter):
    title = _("Consent date")

    parameter_name = "consent_datetime"
    field_name = "consent_datetime"
