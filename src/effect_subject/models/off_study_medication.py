"""Have you prescribed fluconazole consolidation therapy?
Yes, 800mg daily
Yes, 400mg daily
Yes, other dose
No
Notes on fluconazole
________________ (mandatory if C or D above)"""

from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class OffStudyMedication(CrfModelMixin, edc_models.BaseUuidModel):
    # flucon_dose
    # flucyt_dose

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Study medication"
        verbose_name_plural = "Study medication"
