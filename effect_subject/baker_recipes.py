from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_bakery.recipe import Recipe

from .models import (
    Followup,
    SignsAndSymptoms,
    StudyTreatment,
    SubjectRequisition,
    SubjectVisit,
)

fake = Faker()

followup = Recipe(Followup)

signsandsymptoms = Recipe(SignsAndSymptoms)

studytreatment = Recipe(StudyTreatment)

subjectvisit = Recipe(SubjectVisit, reason=SCHEDULED)

subjectrequisition = Recipe(SubjectRequisition)
