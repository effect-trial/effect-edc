from django.db import models
from edc_lab.model_mixins import requisition_fk_options
from edc_lab_panel.panels import sputum_panel
from edc_microbiology.model_mixins import (
    SputumAfbModelMixin,
    SputumCultureModelMixin,
    SputumGenexpertModelMixin,
    UrinaryLamModelMixin,
)
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class TbDiagnostics(
    UrinaryLamModelMixin,
    SputumGenexpertModelMixin,
    SputumCultureModelMixin,
    SputumAfbModelMixin,
    CrfModelMixin,
    edc_models.BaseUuidModel,
):
    sputum_requisition = models.ForeignKey(
        verbose_name="Sputum requisition",
        limit_choices_to={"panel__name": sputum_panel.name},
        **{k: v for k, v in requisition_fk_options.items() if k != "verbose_name"},
    )

    comment = models.TextField(verbose_name="Any additional comment", null=True, blank=True)

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "TB Diagnostics"
        verbose_name_plural = "TB Diagnostics"
