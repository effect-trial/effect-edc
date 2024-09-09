from edc_visit_schedule.visit import Crf, CrfCollection

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

crfs_prn_baseline = CrfCollection(
    Crf(show_order=75, model="effect_subject.vitalsigns"),
    Crf(show_order=205, model="effect_subject.bloodresultsfbc"),
    Crf(show_order=215, model="effect_subject.bloodresultschem"),
    Crf(show_order=235, model="effect_subject.chestxray"),
    Crf(show_order=245, model="effect_subject.lpcsf"),
    Crf(show_order=255, model="effect_subject.tbdiagnostics"),
    Crf(show_order=345, model="effect_subject.bloodculture"),
    Crf(show_order=365, model="effect_subject.histopathology"),
    Crf(show_order=406, model="effect_subject.healtheconomicsevent"),
    Crf(show_order=505, model="effect_subject.clinicalnote"),
    name="prn_baseline",
)

crfs_prn_followup = CrfCollection(
    Crf(show_order=55, model="effect_subject.studymedicationfollowup"),
    *[crf for crf in crfs_prn_baseline],
    name="prn_followup",
)

crfs_unscheduled = CrfCollection(
    Crf(show_order=70, model="effect_subject.vitalsigns", required=False),
    Crf(show_order=80, model="effect_subject.mentalstatus"),
    Crf(show_order=90, model="effect_subject.signsandsymptoms"),
    Crf(show_order=100, model="effect_subject.diagnoses"),
    Crf(show_order=401, model="effect_subject.healtheconomicsevent"),
    Crf(show_order=500, model="effect_subject.clinicalnote"),
    name="unscheduled",
)

crfs_unscheduled_lt_d14 = CrfCollection(
    *[crf for crf in crfs_unscheduled],
    Crf(show_order=602, model="effect_subject.adherencestagetwo"),
    name="unscheduled_lt_d14",
)

crfs_unscheduled_gte_d14 = CrfCollection(
    *[crf for crf in crfs_unscheduled],
    Crf(show_order=604, model="effect_subject.adherencestagefour"),
    name="unscheduled_gte_d14",
)

crfs_missed = CrfCollection(
    Crf(show_order=10, model="effect_subject.subjectvisitmissed"),
    name="missed",
)

crfs_d01 = CrfCollection(
    Crf(show_order=40, model="effect_subject.arvhistory"),
    Crf(show_order=60, model="effect_subject.participanthistory"),
    Crf(show_order=70, model="effect_subject.vitalsigns"),
    Crf(show_order=80, model="effect_subject.mentalstatus"),
    Crf(show_order=90, model="effect_subject.signsandsymptoms"),
    Crf(show_order=99, model="effect_subject.studymedicationbaseline"),
    Crf(show_order=200, model="effect_subject.bloodresultsfbc"),
    Crf(show_order=210, model="effect_subject.bloodresultschem"),
    Crf(show_order=230, model="effect_subject.chestxray", required=False),
    Crf(show_order=240, model="effect_subject.lpcsf", required=False),
    Crf(show_order=250, model="effect_subject.tbdiagnostics", required=False),
    Crf(show_order=400, model="effect_subject.healtheconomics"),
    Crf(show_order=500, model="effect_subject.clinicalnote"),
    Crf(show_order=601, model="effect_subject.adherencestageone"),
    name=DAY01,
)

crfs_d03 = CrfCollection(
    Crf(show_order=70, model="effect_subject.vitalsigns", required=False),
    # TODO: ???Remove ECOG/CGS symptoms for tel visits
    Crf(show_order=80, model="effect_subject.mentalstatus"),
    # TODO: ???Remove neurological symptoms for tel visits
    Crf(show_order=90, model="effect_subject.signsandsymptoms"),
    Crf(show_order=100, model="effect_subject.diagnoses"),
    Crf(show_order=230, model="effect_subject.chestxray", required=False),
    Crf(show_order=240, model="effect_subject.lpcsf", required=False),
    Crf(show_order=250, model="effect_subject.tbdiagnostics", required=False),
    Crf(show_order=602, model="effect_subject.adherencestagetwo"),
    name=DAY03,
)

crfs_d09 = CrfCollection(
    Crf(show_order=70, model="effect_subject.vitalsigns", required=False),
    Crf(show_order=80, model="effect_subject.mentalstatus"),
    Crf(show_order=90, model="effect_subject.signsandsymptoms"),
    Crf(show_order=100, model="effect_subject.diagnoses"),
    Crf(show_order=230, model="effect_subject.chestxray", required=False),
    Crf(show_order=240, model="effect_subject.lpcsf", required=False),
    Crf(show_order=250, model="effect_subject.tbdiagnostics", required=False),
    Crf(show_order=602, model="effect_subject.adherencestagetwo"),
    name=DAY09,
)

crfs_d14 = CrfCollection(
    Crf(show_order=70, model="effect_subject.vitalsigns", required=False),
    Crf(show_order=50, model="effect_subject.studymedicationfollowup"),
    Crf(show_order=80, model="effect_subject.mentalstatus"),
    Crf(show_order=90, model="effect_subject.signsandsymptoms"),
    Crf(show_order=100, model="effect_subject.diagnoses"),
    Crf(show_order=110, model="effect_subject.arvtreatment"),
    Crf(show_order=120, model="effect_subject.participanttreatment"),
    Crf(show_order=200, model="effect_subject.bloodresultsfbc"),
    Crf(show_order=230, model="effect_subject.chestxray", required=False),
    Crf(show_order=240, model="effect_subject.lpcsf", required=False),
    Crf(show_order=250, model="effect_subject.tbdiagnostics", required=False),
    Crf(show_order=500, model="effect_subject.clinicalnote"),
    Crf(show_order=603, model="effect_subject.adherencestagethree"),
    name=DAY14,
)

crfs_w04 = CrfCollection(
    Crf(show_order=70, model="effect_subject.vitalsigns", required=False),
    Crf(show_order=80, model="effect_subject.mentalstatus"),
    Crf(show_order=90, model="effect_subject.signsandsymptoms"),
    Crf(show_order=100, model="effect_subject.diagnoses"),
    Crf(show_order=230, model="effect_subject.chestxray", required=False),
    Crf(show_order=240, model="effect_subject.lpcsf", required=False),
    Crf(show_order=250, model="effect_subject.tbdiagnostics", required=False),
    Crf(show_order=604, model="effect_subject.adherencestagefour"),
    name=WEEK04,
)

crfs_w10 = CrfCollection(
    Crf(show_order=50, model="effect_subject.studymedicationfollowup"),
    Crf(show_order=70, model="effect_subject.vitalsigns", required=False),
    Crf(show_order=80, model="effect_subject.mentalstatus"),
    Crf(show_order=90, model="effect_subject.signsandsymptoms"),
    Crf(show_order=100, model="effect_subject.diagnoses"),
    Crf(show_order=230, model="effect_subject.chestxray", required=False),
    Crf(show_order=240, model="effect_subject.lpcsf", required=False),
    Crf(show_order=250, model="effect_subject.tbdiagnostics", required=False),
    Crf(show_order=604, model="effect_subject.adherencestagefour"),
    name=WEEK10,
)

crfs_w16 = CrfCollection(
    Crf(show_order=70, model="effect_subject.vitalsigns", required=False),
    Crf(show_order=80, model="effect_subject.mentalstatus"),
    Crf(show_order=90, model="effect_subject.signsandsymptoms"),
    Crf(show_order=100, model="effect_subject.diagnoses"),
    Crf(show_order=230, model="effect_subject.chestxray", required=False),
    Crf(show_order=240, model="effect_subject.lpcsf", required=False),
    Crf(show_order=250, model="effect_subject.tbdiagnostics", required=False),
    Crf(show_order=604, model="effect_subject.adherencestagefour"),
    name=WEEK16,
)

crfs_w24 = CrfCollection(
    Crf(show_order=70, model="effect_subject.vitalsigns", required=False),
    Crf(show_order=80, model="effect_subject.mentalstatus"),
    Crf(show_order=90, model="effect_subject.signsandsymptoms"),
    Crf(show_order=100, model="effect_subject.diagnoses"),
    Crf(show_order=230, model="effect_subject.chestxray", required=False),
    Crf(show_order=240, model="effect_subject.lpcsf", required=False),
    Crf(show_order=250, model="effect_subject.tbdiagnostics", required=False),
    Crf(show_order=400, model="effect_subject.healtheconomics"),
    # TODO: Termination Form CRF
    Crf(show_order=604, model="effect_subject.adherencestagefour"),
    name=WEEK24,
)
