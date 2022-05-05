from .study_medication import StudyMedication


class StudyMedicationBaseline(StudyMedication):
    class Meta:
        proxy = True
        verbose_name = "Study medication (Baseline)"
        verbose_name_plural = "Study medication (Baseline)"
