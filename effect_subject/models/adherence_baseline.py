from .adherence import Adherence


class AdherenceBaseline(Adherence):
    """Adherence CRF completed at baseline."""

    class Meta:
        proxy = True
        verbose_name = "Adherence (Baseline)"
        verbose_name_plural = "Adherence (Baseline)"
