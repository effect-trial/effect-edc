from __future__ import annotations

from decimal import Decimal

from edc_crf.model_mixins import CrfWithActionModelMixin
from edc_egfr.egfr import Egfr as BaseEgfr
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
from edc_model.models import BaseUuidModel

from effect_labs.panels import chemistry_panel

from ...constants import BLOOD_RESULTS_CHEM_ACTION
from ...utils import get_weight_in_kgs

# TODO: align model mixins with panel


class Egfr(BaseEgfr):
    def on_percent_drop_threshold_reached(self) -> None:
        return None


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
    BaseUuidModel,
):
    action_name = BLOOD_RESULTS_CHEM_ACTION

    lab_panel = chemistry_panel

    egfr_formula_name: str = "cockcroft-gault"
    egfr_cls = Egfr

    def get_weight_in_kgs_for_egfr(self) -> Decimal | None:
        """Override method from EgfrModelMixin"""
        return get_weight_in_kgs(subject_visit=self.subject_visit)

    class Meta(CrfWithActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Blood Result: Chemistry"
        verbose_name_plural = "Blood Results: Chemistry"
