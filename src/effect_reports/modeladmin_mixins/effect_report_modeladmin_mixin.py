from contextlib import suppress

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from edc_appointment.models import Appointment

MAX_VISIT_CODE_SEQUENCE = 10


class EffectReportModelAdminMixin:
    @admin.display(description="subject", ordering="subject_identifier")
    def subject_dashboard(self, obj=None) -> str:
        kwargs = self.get_subject_dashboard_url_kwargs(obj)
        url = reverse(self.get_subject_dashboard_url_name(obj=obj), kwargs=kwargs)
        context = dict(
            title=_("Go to subject dashboard for {subject_identifier}").format(
                subject_identifier=obj.subject_identifier
            ),
            url=url,
            label=format_html("{}", obj.subject_identifier),
        )
        return render_to_string("edc_subject_dashboard/dashboard_button.html", context=context)

    @admin.display(description="visit")
    def visit_dashboard(self, obj=None) -> str:
        kwargs = self.get_subject_dashboard_url_kwargs(obj)
        with suppress(ObjectDoesNotExist):
            kwargs.update(
                appointment=str(
                    Appointment.objects.get(
                        subject_identifier=obj.subject_identifier,
                        visit_code=obj.visit_code,
                        visit_code_sequence=obj.visit_code_sequence,
                    ).id,
                ),
            )
        url = reverse(self.get_subject_dashboard_url_name(obj=obj), kwargs=kwargs)
        context = dict(
            title=_(
                "Go to visit {visit_code}.{visit_code_sequence} for {subject_identifier}"
            ).format(
                visit_code=obj.visit_code,
                visit_code_sequence=obj.visit_code_sequence,
                subject_identifier=obj.subject_identifier,
            ),
            url=url,
            label=format_html(
                "{}.{}{padding}",
                obj.visit_code,
                obj.visit_code_sequence,
                padding=(
                    mark_safe("&nbsp;")  # nosec #B703 # B308
                    if obj.visit_code_sequence < MAX_VISIT_CODE_SEQUENCE
                    else ""
                ),
            ),
        )
        return render_to_string("edc_subject_dashboard/dashboard_button.html", context=context)
