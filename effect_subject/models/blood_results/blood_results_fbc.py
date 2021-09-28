from edc_blood_results import BLOOD_RESULTS_FBC_ACTION
from edc_blood_results.model_mixins import (
    BloodResultsModelMixin,
    HaemoglobinModelMixin,
    HctModelMixin,
    MchcModelMixin,
    MchModelMixin,
    McvModelMixin,
    PlateletsModelMixin,
    RbcModelMixin,
    RequisitionModelMixin,
    WbcModelMixin,
)
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_lab_panel.panels import fbc_panel
from edc_model import models as edc_models


class BloodResultsFbc(
    CrfWithActionModelMixin,
    RequisitionModelMixin,
    HaemoglobinModelMixin,
    HctModelMixin,
    RbcModelMixin,
    WbcModelMixin,
    PlateletsModelMixin,
    MchModelMixin,
    MchcModelMixin,
    McvModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    action_name = BLOOD_RESULTS_FBC_ACTION
    tracking_identifier_prefix = "FB"

    lab_panel = fbc_panel

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: FBC"
        verbose_name_plural = "Blood Results: FBC"
