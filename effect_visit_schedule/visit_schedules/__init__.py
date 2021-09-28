import sys

from django.core.management import color_style
from edc_visit_schedule import site_visit_schedules

from effect_edc.effect_version import get_effect_version

style = color_style()

if get_effect_version() == 2:
    from .phase_two import SCHEDULE, VISIT_SCHEDULE, schedule, visit_schedule

    sys.stdout.write(
        style.SUCCESS("Notice: loading visit schedule for phase 2 **** \n")
    )
elif get_effect_version() == 3:
    from .phase_three import SCHEDULE, VISIT_SCHEDULE, schedule, visit_schedule

    sys.stdout.write(
        style.SUCCESS("Notice: loading visit schedule for phase 3 **** \n")
    )
site_visit_schedules.register(visit_schedule)
