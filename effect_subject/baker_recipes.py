from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_bakery.recipe import Recipe

from .models import (
    ChestXray,
    Diagnoses,
    MentalStatus,
    ParticipantTreatment,
    SignsAndSymptoms,
    SubjectRequisition,
    SubjectVisit,
    VitalSigns,
)

fake = Faker()

chestxray = Recipe(ChestXray)

diagnoses = Recipe(Diagnoses)

mentalstatus = Recipe(MentalStatus)

participanttreatment = Recipe(ParticipantTreatment)

signsandsymptoms = Recipe(SignsAndSymptoms)

subjectrequisition = Recipe(SubjectRequisition)

subjectvisit = Recipe(SubjectVisit, reason=SCHEDULED)

vitalsigns = Recipe(VitalSigns)
