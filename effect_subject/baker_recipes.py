from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_bakery.recipe import Recipe

from .models import (
    ChestXray,
    Diagnoses,
    MentalStatus,
    PatientTreatment,
    SignsAndSymptoms,
    SubjectRequisition,
    SubjectVisit,
    VitalSigns,
)

fake = Faker()

chestxray = Recipe(ChestXray)

diagnoses = Recipe(Diagnoses)

mentalstatus = Recipe(MentalStatus)

signsandsymptoms = Recipe(SignsAndSymptoms)

subjectvisit = Recipe(SubjectVisit, reason=SCHEDULED)

subjectrequisition = Recipe(SubjectRequisition)

patienttreatment = Recipe(PatientTreatment)

vitalsigns = Recipe(VitalSigns)
