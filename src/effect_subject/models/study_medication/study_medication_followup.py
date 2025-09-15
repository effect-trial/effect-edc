from .study_medication import StudyMedication


class StudyMedicationFollowup(StudyMedication):
    class Meta:
        proxy = True
        verbose_name = "Study Medication"
        verbose_name_plural = "Study Medication"
