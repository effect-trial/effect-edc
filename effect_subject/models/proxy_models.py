from .adherence import Adherence


class AdherenceStageOne(Adherence):
    """Adherence CRF completed at baseline (in-person)."""

    class Meta:
        proxy = True
        verbose_name = "Adherence: Day 1"
        verbose_name_plural = "Adherence: Day 1"


class AdherenceStageTwo(Adherence):
    """Adherence CRF completed at d3 and d9 (telephone)."""

    class Meta:
        proxy = True
        verbose_name = "Adherence: On study"
        verbose_name_plural = "Adherence: On study"


class AdherenceStageThree(Adherence):
    """Adherence CRF completed at d14 (in-person)."""

    class Meta:
        proxy = True
        verbose_name = "Adherence: Day 14"
        verbose_name_plural = "Adherence: Day 14"


class AdherenceStageFour(Adherence):
    """Adherence CRF completed after d14 (telephone)."""

    class Meta:
        proxy = True
        verbose_name = "Adherence: Day 14+"
        verbose_name_plural = "Adherence: Day 14+"
