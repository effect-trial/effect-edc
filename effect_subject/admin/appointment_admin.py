from __future__ import annotations

from django.contrib import admin
from edc_appointment.admin import AppointmentAdmin as BaseAdmin
from edc_appointment.admin_site import edc_appointment_admin
from edc_appointment.models import Appointment

from ..choices import APPT_REASON_CHOICES

edc_appointment_admin.unregister(Appointment)


@admin.register(Appointment, site=edc_appointment_admin)
class AppointmentAdmin(BaseAdmin):
    def get_appt_reason_choices(self, request) -> tuple[str, str]:
        return APPT_REASON_CHOICES
