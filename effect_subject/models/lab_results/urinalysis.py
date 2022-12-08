from django.db import models
from edc_crf.model_mixins import CrfWithActionModelMixin
from edc_lab.model_mixins import CrfWithRequisitionModelMixin, requisition_fk_options
from edc_lab_results.constants import URINALYSIS_ACTION
from edc_lab_results.model_mixins import BloodResultsModelMixin, ProteinuriaModelMixin
from edc_model import models as edc_models

from effect_labs.panels import urinalysis_panel


class Urinalysis(
    CrfWithActionModelMixin,
    CrfWithRequisitionModelMixin,
    ProteinuriaModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    action_name = URINALYSIS_ACTION

    lab_panel = urinalysis_panel

    requisition = models.ForeignKey(
        limit_choices_to={"panel__name": urinalysis_panel.name}, **requisition_fk_options
    )

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Urinalysis"
        verbose_name_plural = "Urinalysis"
