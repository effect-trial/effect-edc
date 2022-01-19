from edc_visit_schedule import Crf, FormsCollection

from effect_visit_schedule.constants import (
    DAY01,
    DAY03,
    DAY09,
    DAY14,
    WEEK04,
    WEEK10,
    WEEK16,
    WEEK24,
)

crfs_prn = FormsCollection(
    Crf(show_order=10, model="effect_subject.bloodresultsfbc"),
    Crf(show_order=240, model="effect_subject.bloodresultsrft"),
    Crf(show_order=250, model="effect_subject.bloodresultslft"),
    name="prn",
)

crfs_unscheduled = FormsCollection(
    Crf(show_order=10, model="effect_subject.followup"),
    name="unscheduled",
)

crfs_missed = FormsCollection(
    Crf(show_order=10, model="effect_subject.subjectvisitmissed"),
    name="missed",
)
crfs_d01 = FormsCollection(
    Crf(show_order=10, model="effect_subject.followup"),
    Crf(show_order=20, model="effect_subject.signsandsymptoms"),
    Crf(show_order=30, model="effect_subject.neurological"),
    Crf(show_order=40, model="effect_subject.mentalstatus"),
    Crf(show_order=50, model="effect_subject.vitalsigns"),
    Crf(show_order=60, model="effect_subject.diagnoses"),
    Crf(show_order=70, model="effect_subject.chestxray"),
    Crf(show_order=80, model="effect_subject.arvtreatment"),
    Crf(show_order=90, model="effect_subject.studytreatment"),
    Crf(show_order=100, model="effect_subject.bloodresultsfbc"),
    Crf(show_order=110, model="effect_subject.clinicalnote"),
    name=DAY01,
)

crfs_d03 = FormsCollection(
    Crf(show_order=10, model="effect_subject.followup"),
    name=DAY03,
)

crfs_d09 = FormsCollection(
    Crf(show_order=10, model="effect_subject.followup"),
    name=DAY09,
)

crfs_d14 = FormsCollection(
    Crf(show_order=10, model="effect_subject.followup"),
    name=DAY14,
)


crfs_w04 = FormsCollection(
    Crf(show_order=10, model="effect_subject.followup"),
    name=WEEK04,
)

crfs_w10 = FormsCollection(
    Crf(show_order=10, model="effect_subject.followup"),
    name=WEEK10,
)

crfs_w16 = FormsCollection(
    Crf(show_order=10, model="effect_subject.followup"),
    name=WEEK16,
)

crfs_w24 = FormsCollection(
    Crf(show_order=10, model="effect_subject.followup"),
    name=WEEK24,
)
