from edc_crf.model_mixins import CrfWithActionModelMixin
from edc_egfr.model_mixins import EgfrModelMixin
from edc_lab.model_mixins import CrfWithRequisitionModelMixin
from edc_lab_results.model_mixins import (
    AlbuminModelMixin,
    AlpModelMixin,
    AltModelMixin,
    AmylaseModelMixin,
    AstModelMixin,
    BloodResultsModelMixin,
    CreatinineModelMixin,
    CrpModelMixin,
    GgtModelMixin,
    MagnesiumModelMixin,
    PotassiumModelMixin,
    TotalBilirubinModelMixin,
    UreaModelMixin,
    UricAcidModelMixin,
)
from edc_model import models as edc_models

from effect_labs.panels import chemistry_panel

from ...constants import BLOOD_RESULTS_CHEM_ACTION

# TODO: align model mixins with panel


class BloodResultsChem(
    CrfWithActionModelMixin,
    CrfWithRequisitionModelMixin,
    AlbuminModelMixin,
    AlpModelMixin,
    AltModelMixin,
    AmylaseModelMixin,
    AstModelMixin,
    CreatinineModelMixin,
    CrpModelMixin,
    EgfrModelMixin,
    MagnesiumModelMixin,
    PotassiumModelMixin,
    TotalBilirubinModelMixin,
    UreaModelMixin,
    UricAcidModelMixin,
    GgtModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    action_name = BLOOD_RESULTS_CHEM_ACTION

    lab_panel = chemistry_panel

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: Chemistry"
        verbose_name_plural = "Blood Results: Chemistry"
