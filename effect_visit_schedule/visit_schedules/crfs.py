from edc_visit_schedule import Crf, FormsCollection
from edc_visit_schedule.constants import (
    DAY1,
    MONTH1,
    MONTH3,
    MONTH6,
    MONTH9,
    MONTH12,
    MONTH15,
    MONTH18,
    MONTH21,
    MONTH24,
    MONTH27,
    MONTH30,
    MONTH33,
    MONTH36,
    WEEK2,
)

crfs_prn = FormsCollection(
    Crf(show_order=10, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=220, model="meta_subject.bloodresultsglu"),
    Crf(show_order=230, model="meta_subject.bloodresultshba1c"),
    Crf(show_order=240, model="meta_subject.bloodresultsrft"),
    Crf(show_order=250, model="meta_subject.bloodresultslft"),
    Crf(show_order=260, model="meta_subject.bloodresultslipid"),
    Crf(show_order=270, model="meta_subject.hepatitistest"),
    Crf(show_order=280, model="meta_subject.malariatest"),
    Crf(show_order=290, model="meta_subject.urinedipsticktest"),
    Crf(show_order=360, model="meta_subject.concomitantmedication"),
    name="prn",
)

crfs_unscheduled = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=20, model="meta_subject.followupexamination"),
    Crf(show_order=30, model="meta_subject.medicationadherence"),
    Crf(show_order=200, model="meta_subject.bloodresultsglu"),
    name="unscheduled",
)

crfs_missed = FormsCollection(
    Crf(show_order=10, model="meta_subject.subjectvisitmissed"),
    name="missed",
)
crfs_d1 = FormsCollection(
    Crf(show_order=100, model="effect_subject.patienthistory"),
    Crf(show_order=150, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.glucose"),
    Crf(show_order=250, model="effect_subject.bloodresultsfbc"),
    Crf(show_order=300, model="effect_subject.bloodresultsrft"),
    Crf(show_order=350, model="effect_subject.bloodresultslft"),
    Crf(show_order=400, model="effect_subject.bloodresultslipid"),
    Crf(show_order=450, model="effect_subject.bloodresultshba1c"),
    Crf(show_order=500, model="effect_subject.malariatest"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=DAY1,
)

crfs_w2 = FormsCollection(
    Crf(show_order=100, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.glucose"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=WEEK2,
)

crfs_1m = FormsCollection(
    Crf(show_order=100, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.bloodresultsglu"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=MONTH1,
)

crfs_3m = FormsCollection(
    Crf(show_order=150, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.bloodresultsglu"),
    Crf(show_order=300, model="effect_subject.bloodresultsrft"),
    Crf(show_order=350, model="effect_subject.bloodresultslft"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=MONTH3,
)

crfs_6m = FormsCollection(
    Crf(show_order=150, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.bloodresultsglu"),
    Crf(show_order=250, model="effect_subject.bloodresultsfbc"),
    Crf(show_order=300, model="effect_subject.bloodresultsrft"),
    Crf(show_order=350, model="effect_subject.bloodresultslft"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=MONTH6,
)

crfs_9m = FormsCollection(
    Crf(show_order=150, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.bloodresultsglu"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=MONTH9,
)

crfs_12m = FormsCollection(
    Crf(show_order=150, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.glucose"),
    Crf(show_order=250, model="effect_subject.bloodresultsfbc"),
    Crf(show_order=300, model="effect_subject.bloodresultsrft"),
    Crf(show_order=350, model="effect_subject.bloodresultslft"),
    Crf(show_order=400, model="effect_subject.bloodresultslipid"),
    Crf(show_order=450, model="effect_subject.bloodresultshba1c"),
    Crf(show_order=500, model="effect_subject.malariatest"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=MONTH12,
)

crfs_15m = FormsCollection(
    Crf(show_order=150, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.bloodresultsglu"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=MONTH15,
)

crfs_18m = FormsCollection(
    Crf(show_order=150, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.bloodresultsglu"),
    Crf(show_order=250, model="effect_subject.bloodresultsfbc"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=MONTH18,
)

crfs_21m = FormsCollection(
    Crf(show_order=150, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.bloodresultsglu"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=MONTH21,
)

crfs_24m = FormsCollection(
    Crf(show_order=150, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.glucose"),
    Crf(show_order=250, model="effect_subject.bloodresultsfbc"),
    Crf(show_order=300, model="effect_subject.bloodresultsrft"),
    Crf(show_order=350, model="effect_subject.bloodresultslft"),
    Crf(show_order=400, model="effect_subject.bloodresultslipid"),
    Crf(show_order=450, model="effect_subject.bloodresultshba1c"),
    Crf(show_order=500, model="effect_subject.malariatest"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=MONTH24,
)

crfs_27m = FormsCollection(
    Crf(show_order=150, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.bloodresultsglu"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=MONTH27,
)

crfs_30m = FormsCollection(
    Crf(show_order=150, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.bloodresultsglu"),
    Crf(show_order=250, model="effect_subject.bloodresultsfbc"),
    Crf(show_order=300, model="effect_subject.bloodresultsrft"),
    Crf(show_order=350, model="effect_subject.bloodresultslft"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=MONTH30,
)

crfs_33m = FormsCollection(
    Crf(show_order=150, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.bloodresultsglu"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=MONTH33,
)

crfs_36m = FormsCollection(
    Crf(show_order=150, model="effect_subject.physicalexam"),
    Crf(show_order=200, model="effect_subject.glucose"),
    Crf(show_order=250, model="effect_subject.bloodresultsfbc"),
    Crf(show_order=300, model="effect_subject.bloodresultsrft"),
    Crf(show_order=350, model="effect_subject.bloodresultslft"),
    Crf(show_order=400, model="effect_subject.bloodresultslipid"),
    Crf(show_order=450, model="effect_subject.bloodresultshba1c"),
    Crf(show_order=500, model="effect_subject.malariatest"),
    Crf(show_order=550, model="effect_subject.medicationadherence"),
    Crf(show_order=600, model="effect_subject.studymedication"),
    name=MONTH36,
)
