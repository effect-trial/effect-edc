from django.db import models
from edc_crf.model_mixins import CrfWithActionModelMixin
from edc_lab.model_mixins import CrfWithRequisitionModelMixin, requisition_fk_options
from edc_lab_results import BLOOD_RESULTS_FBC_ACTION
from edc_lab_results.model_mixins import (
    BloodResultsModelMixin,
    HaemoglobinModelMixin,
    LymphocyteDiffModelMixin,
    LymphocyteModelMixin,
    NeutrophilDiffModelMixin,
    NeutrophilModelMixin,
    PlateletsModelMixin,
    RbcModelMixin,
    WbcModelMixin,
)
from edc_model import models as edc_models

from effect_labs.panels import fbc_panel


class BloodResultsFbc(
    CrfWithActionModelMixin,
    CrfWithRequisitionModelMixin,
    HaemoglobinModelMixin,
    RbcModelMixin,
    WbcModelMixin,
    PlateletsModelMixin,
    NeutrophilModelMixin,
    NeutrophilDiffModelMixin,
    LymphocyteDiffModelMixin,
    LymphocyteModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    action_name = BLOOD_RESULTS_FBC_ACTION

    lab_panel = fbc_panel

    requisition = models.ForeignKey(
        limit_choices_to={"panel__name": fbc_panel.name},
        **requisition_fk_options,
    )

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: FBC"
        verbose_name_plural = "Blood Results: FBC"
