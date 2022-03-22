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
    Crf(show_order=300, model="effect_subject.microbiology"),
    Crf(show_order=310, model="effect_subject.lpcsf"),
    Crf(show_order=340, model="effect_subject.bloodculture"),
    Crf(show_order=360, model="effect_subject.histopathology"),
    Crf(show_order=400, model="effect_subject.healtheconomics"),
    name="prn",
)

crfs_unscheduled = FormsCollection(
    Crf(show_order=65, model="effect_subject.adherence"),
    # TODO: Use correct adherence form for unscheduled visits
    Crf(show_order=70, model="effect_subject.adherencestageone"),
    Crf(show_order=75, model="effect_subject.adherencestagetwo"),
    Crf(show_order=80, model="effect_subject.adherencestagethree"),
    Crf(show_order=85, model="effect_subject.adherencestagefour"),
    name="unscheduled",
)

crfs_missed = FormsCollection(
    Crf(show_order=10, model="effect_subject.subjectvisitmissed"),
    name="missed",
)
crfs_d01 = FormsCollection(
    Crf(show_order=10, model="effect_subject.adherencestageone"),
    Crf(show_order=20, model="effect_subject.signsandsymptoms"),
    Crf(show_order=40, model="effect_subject.mentalstatus"),
    Crf(show_order=45, model="effect_subject.medicalhistory"),
    Crf(show_order=50, model="effect_subject.arvhistory"),
    Crf(show_order=55, model="effect_subject.vitalsigns"),
    Crf(show_order=60, model="effect_subject.diagnoses"),
    Crf(show_order=70, model="effect_subject.chestxray"),
    Crf(show_order=80, model="effect_subject.arvtreatment"),
    Crf(show_order=85, model="effect_subject.patienthistory"),
    Crf(show_order=90, model="effect_subject.patienttreatment"),
    Crf(show_order=100, model="effect_subject.bloodresultsfbc"),
    Crf(show_order=140, model="effect_subject.lpcsf"),
    Crf(show_order=160, model="effect_subject.microbiology"),
    Crf(show_order=340, model="effect_subject.bloodculture"),
    Crf(show_order=360, model="effect_subject.histopathology"),
    Crf(show_order=400, model="effect_subject.healtheconomics"),
    Crf(show_order=500, model="effect_subject.clinicalnote"),
    name=DAY01,
)

crfs_d03 = FormsCollection(
    Crf(show_order=10, model="effect_subject.adherencestagetwo"),
    # TODO: ???Remove neurological symptoms for tel visits
    Crf(show_order=20, model="effect_subject.signsandsymptoms"),
    # TODO: ???Remove ECOG/CGS symptoms for tel visits
    Crf(show_order=40, model="effect_subject.mentalstatus"),
    name=DAY03,
)

crfs_d09 = FormsCollection(
    Crf(show_order=10, model="effect_subject.adherencestagetwo"),
    Crf(show_order=20, model="effect_subject.signsandsymptoms"),
    Crf(show_order=40, model="effect_subject.mentalstatus"),
    name=DAY09,
)

crfs_d14 = FormsCollection(
    Crf(show_order=10, model="effect_subject.adherencestagethree"),
    Crf(show_order=20, model="effect_subject.signsandsymptoms"),
    Crf(show_order=40, model="effect_subject.mentalstatus"),
    Crf(show_order=80, model="effect_subject.arvtreatment"),
    Crf(show_order=90, model="effect_subject.patienttreatment"),
    Crf(show_order=100, model="effect_subject.bloodresultsfbc"),
    Crf(show_order=400, model="effect_subject.healtheconomics"),
    Crf(show_order=500, model="effect_subject.clinicalnote"),
    name=DAY14,
)

crfs_w04 = FormsCollection(
    Crf(show_order=10, model="effect_subject.adherencestagefour"),
    Crf(show_order=20, model="effect_subject.signsandsymptoms"),
    Crf(show_order=40, model="effect_subject.mentalstatus"),
    name=WEEK04,
)

crfs_w10 = FormsCollection(
    Crf(show_order=10, model="effect_subject.adherencestagefour"),
    Crf(show_order=20, model="effect_subject.signsandsymptoms"),
    Crf(show_order=40, model="effect_subject.mentalstatus"),
    name=WEEK10,
)

crfs_w16 = FormsCollection(
    Crf(show_order=10, model="effect_subject.adherencestagefour"),
    Crf(show_order=20, model="effect_subject.signsandsymptoms"),
    Crf(show_order=40, model="effect_subject.mentalstatus"),
    name=WEEK16,
)

crfs_w24 = FormsCollection(
    Crf(show_order=10, model="effect_subject.adherencestagefour"),
    Crf(show_order=20, model="effect_subject.signsandsymptoms"),
    Crf(show_order=40, model="effect_subject.mentalstatus"),
    Crf(show_order=400, model="effect_subject.healtheconomics"),
    # TODO: Termination Form CRF
    name=WEEK24,
)
