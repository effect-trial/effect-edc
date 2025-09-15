from dateutil.relativedelta import relativedelta
from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.visit import Visit as BaseVisit

from effect_consent.consents import consent_v1, consent_v2

from ..constants import (
    DAY01,
    DAY03,
    DAY09,
    DAY14,
    SCHEDULE,
    WEEK04,
    WEEK10,
    WEEK16,
    WEEK24,
)
from .crfs import (
    crfs_d01,
    crfs_d03,
    crfs_d09,
    crfs_d14,
    crfs_missed,
    crfs_prn_baseline,
    crfs_prn_followup,
    crfs_unscheduled_gte_d14,
    crfs_unscheduled_lt_d14,
    crfs_w04,
    crfs_w10,
    crfs_w16,
    crfs_w24,
)
from .crfs import crfs_unscheduled as default_crfs_unscheduled
from .requisitions import requisitions_d01, requisitions_d14
from .requisitions import requisitions_prn as default_requisitions_prn
from .requisitions import requisitions_unscheduled as default_requisitions_unscheduled

__all__ = ["schedule"]


class Visit(BaseVisit):
    def __init__(
        self,
        crfs_unscheduled=None,
        requisitions_unscheduled=None,
        crfs_prn=None,
        requisitions_prn=None,
        allow_unscheduled=None,
        **kwargs,
    ):
        super().__init__(
            allow_unscheduled=True if allow_unscheduled is None else allow_unscheduled,
            crfs_unscheduled=crfs_unscheduled or default_crfs_unscheduled,
            requisitions_unscheduled=requisitions_unscheduled
            or default_requisitions_unscheduled,
            crfs_prn=crfs_prn or crfs_prn_followup,
            requisitions_prn=requisitions_prn or default_requisitions_prn,
            crfs_missed=crfs_missed,
            **kwargs,
        )


visit000 = Visit(
    code=DAY01,
    title="Day 1",
    timepoint=0,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    requisitions=requisitions_d01,
    crfs=crfs_d01,
    crfs_prn=crfs_prn_baseline,
    crfs_unscheduled=crfs_unscheduled_lt_d14,
    facility_name="7-day-clinic",
)

visit010 = Visit(
    code=DAY03,
    title="Day 3",
    timepoint=10,
    rbase=relativedelta(days=3 - 1),
    rlower=relativedelta(days=1),
    rupper=relativedelta(days=4),
    crfs=crfs_d03,
    crfs_unscheduled=crfs_unscheduled_lt_d14,
    facility_name="7-day-clinic",
)

visit020 = Visit(
    code=DAY09,
    title="Day 9",
    timepoint=20,
    rbase=relativedelta(days=9 - 1),
    rlower=relativedelta(days=1),
    rupper=relativedelta(days=4),
    crfs=crfs_d09,
    crfs_unscheduled=crfs_unscheduled_lt_d14,
    facility_name="7-day-clinic",
)


visit030 = Visit(
    code=DAY14,
    title="Day 14",
    timepoint=30,
    rbase=relativedelta(days=14 - 1),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=7),
    requisitions=requisitions_d14,
    crfs=crfs_d14,
    crfs_unscheduled=crfs_unscheduled_gte_d14,
    facility_name="7-day-clinic",
)

visit040 = Visit(
    code=WEEK04,
    title="Week 4",
    timepoint=40,
    rbase=relativedelta(weeks=4),
    rlower=relativedelta(days=7),
    rupper=relativedelta(days=(5 * 7) - 1),
    crfs=crfs_w04,
    crfs_unscheduled=crfs_unscheduled_gte_d14,
    facility_name="7-day-clinic",
)

visit050 = Visit(
    code=WEEK10,
    title="Week 10",
    timepoint=50,
    rbase=relativedelta(weeks=10),
    rlower=relativedelta(days=7),
    rupper=relativedelta(days=(5 * 7) - 1),
    crfs=crfs_w10,
    crfs_unscheduled=crfs_unscheduled_gte_d14,
    facility_name="7-day-clinic",
)

visit060 = Visit(
    code=WEEK16,
    title="Week 16",
    timepoint=60,
    rbase=relativedelta(weeks=16),
    rlower=relativedelta(days=7),
    rupper=relativedelta(days=(7 * 7) - 1),
    crfs=crfs_w16,
    crfs_unscheduled=crfs_unscheduled_gte_d14,
    facility_name="7-day-clinic",
)

visit070 = Visit(
    code=WEEK24,
    title="Week 24",
    timepoint=70,
    rbase=relativedelta(weeks=24),
    rlower=relativedelta(days=7),
    rupper=relativedelta(days=(8 * 7) - 1),
    crfs=crfs_w24,
    crfs_unscheduled=crfs_unscheduled_gte_d14,
    facility_name="7-day-clinic",
)


# schedule for new participants
schedule = Schedule(
    name=SCHEDULE,
    verbose_name="Day 1 to Month 6 Follow-up",
    onschedule_model="effect_prn.onschedule",
    offschedule_model="effect_prn.endofstudy",
    consent_definitions=[consent_v1, consent_v2],
)


for visit in [
    visit000,
    visit010,
    visit020,
    visit030,
    visit040,
    visit050,
    visit060,
    visit070,
]:
    schedule.add_visit(visit=visit)
