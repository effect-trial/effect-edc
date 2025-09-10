from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from edc_appointment.models import Appointment


class EffectReportModelAdminMixin(object):

    @admin.display(description="subject", ordering="subject_identifier")
    def subject_dashboard(self, obj=None, label=None) -> str:
        kwargs = self.get_subject_dashboard_url_kwargs(obj)
        url = reverse(self.get_subject_dashboard_url_name(obj=obj), kwargs=kwargs)
        context = dict(
            title=_(f"Go to subject dashboard for {obj.subject_identifier}"),
            url=url,
            label=format_html("{}", obj.subject_identifier),
        )
        return render_to_string("edc_subject_dashboard/dashboard_button.html", context=context)

    @admin.display(description="visit")
    def visit_dashboard(self, obj=None, label=None) -> str:
        kwargs = self.get_subject_dashboard_url_kwargs(obj)
        try:
            kwargs.update(
                appointment=str(
                    Appointment.objects.get(
                        subject_identifier=obj.subject_identifier,
                        visit_code=obj.visit_code,
                        visit_code_sequence=obj.visit_code_sequence,
                    ).id
                )
            )
        except ObjectDoesNotExist:
            pass
        url = reverse(self.get_subject_dashboard_url_name(obj=obj), kwargs=kwargs)
        context = dict(
            title=_(
                f"Go to visit {obj.visit_code}.{obj.visit_code_sequence} "
                f"for {obj.subject_identifier}"
            ),
            url=url,
            label=format_html(
                "{}.{}{padding}",
                obj.visit_code,
                obj.visit_code_sequence,
                padding=(
                    mark_safe("&nbsp;")  # nosec #B703 # B308
                    if obj.visit_code_sequence < 10
                    else ""
                ),
            ),
        )
        return render_to_string("edc_subject_dashboard/dashboard_button.html", context=context)
