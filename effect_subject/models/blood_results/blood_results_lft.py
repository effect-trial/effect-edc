from edc_blood_results import BLOOD_RESULTS_LFT_ACTION
from edc_blood_results.model_mixins import (
    AlbuminModelMixin,
    AlpModelMixin,
    AltModelMixin,
    AmylaseModelMixin,
    AstModelMixin,
    BloodResultsModelMixin,
    GgtModelMixin,
    RequisitionModelMixin,
)
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_lab_panel.panels import lft_panel
from edc_model import models as edc_models


class BloodResultsLft(
    CrfWithActionModelMixin,
    AlbuminModelMixin,
    AlpModelMixin,
    AltModelMixin,
    AmylaseModelMixin,
    AstModelMixin,
    GgtModelMixin,
    RequisitionModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    action_name = BLOOD_RESULTS_LFT_ACTION
    tracking_identifier_prefix = "LF"
    lab_panel = lft_panel

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: LFT"
        verbose_name_plural = "Blood Results: LFT"
