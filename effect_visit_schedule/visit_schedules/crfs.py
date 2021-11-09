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
    Crf(show_order=220, model="effect_subject.bloodresultsglu"),
    Crf(show_order=230, model="effect_subject.bloodresultshba1c"),
    Crf(show_order=240, model="effect_subject.bloodresultsrft"),
    Crf(show_order=250, model="effect_subject.bloodresultslft"),
    Crf(show_order=260, model="effect_subject.bloodresultslipid"),
    Crf(show_order=280, model="effect_subject.malariatest"),
    Crf(show_order=290, model="effect_subject.urinedipsticktest"),
    Crf(show_order=360, model="effect_subject.concomitantmedication"),
    name="prn",
)

crfs_unscheduled = FormsCollection(
    Crf(show_order=10, model="effect_subject.clinicalassessment"),
    name="unscheduled",
)

crfs_missed = FormsCollection(
    Crf(show_order=10, model="effect_subject.subjectvisitmissed"),
    name="missed",
)
crfs_d01 = FormsCollection(
    Crf(show_order=10, model="effect_subject.clinicalassessment"),
    Crf(show_order=250, model="effect_subject.bloodresultsfbc"),
    name=DAY01,
)

crfs_d03 = FormsCollection(
    Crf(show_order=10, model="effect_subject.clinicalassessment"),
    name=DAY03,
)

crfs_d09 = FormsCollection(
    Crf(show_order=10, model="effect_subject.clinicalassessment"),
    name=DAY09,
)

crfs_d14 = FormsCollection(
    Crf(show_order=10, model="effect_subject.clinicalassessment"),
    name=DAY14,
)


crfs_w04 = FormsCollection(
    Crf(show_order=10, model="effect_subject.clinicalassessment"),
    name=WEEK04,
)

crfs_w10 = FormsCollection(
    Crf(show_order=10, model="effect_subject.clinicalassessment"),
    name=WEEK10,
)

crfs_w16 = FormsCollection(
    Crf(show_order=10, model="effect_subject.clinicalassessment"),
    name=WEEK16,
)

crfs_w24 = FormsCollection(
    Crf(show_order=10, model="effect_subject.clinicalassessment"),
    name=WEEK24,
)
