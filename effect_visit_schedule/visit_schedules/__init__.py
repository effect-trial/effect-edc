from edc_visit_schedule import site_visit_schedules

from .schedule import schedule
from .visit_schedule import visit_schedule

site_visit_schedules.register(visit_schedule)
