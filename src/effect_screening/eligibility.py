from __future__ import annotations

from typing import TYPE_CHECKING, Any

from edc_constants.constants import (
    INCOMPLETE,
    NO,
    NOT_DONE,
    NOT_EVALUATED,
    PENDING,
    POS,
    TBD,
    YES,
)
from edc_reportable import CELLS_PER_MICROLITER
from edc_screening.screening_eligibility import (
    ScreeningEligibility as BaseScreeningEligibility,
)
from edc_utils.date import to_local

if TYPE_CHECKING:
    from effect_screening.models import SubjectScreening

CSF_CRAG_PENDING = "CSF CrAg pending"
INCOMPLETE_INCLUSION = "Incomplete inclusion criteria"
INCOMPLETE_EXCLUSION = "Incomplete exclusion criteria"
TWENTY_ONE_DAYS = 21
SIXTY_DAYS = 60
ONE_HUNDRED = 100
EIGHTEEN_YEARS = 18


class ScreeningEligibility(BaseScreeningEligibility):
    eligible_values_list: list = [YES, NO, TBD, PENDING, INCOMPLETE]  # noqa: RUF012

    incomplete_value = INCOMPLETE
    incomplete_display_label = INCOMPLETE

    def __init__(self, model_obj: SubjectScreening = None, **kwargs):
        super().__init__(model_obj=model_obj, **kwargs)

    def assess_eligibility(self) -> None:
        reasons_ineligible: dict[str, str] = {}
        reasons_ineligible.update(**self.review_inclusion(reasons_ineligible))
        reasons_ineligible.update(**self.review_exclusion(reasons_ineligible))

        if self.model_obj.csf_crag_value == PENDING:
            self.eligible = PENDING  # pending csf crag
        elif self.assessment_is_incomplete(reasons_ineligible):
            self.eligible = INCOMPLETE
        else:
            self.eligible = (
                self.is_ineligible_value if reasons_ineligible else self.is_eligible_value
            )
        self.reasons_ineligible = reasons_ineligible

    @staticmethod
    def assessment_is_incomplete(reasons_ineligible: dict[str, str]) -> bool:
        reasons_as_set = set(reasons_ineligible.values())
        return reasons_as_set and reasons_as_set.issubset(
            {INCOMPLETE_INCLUSION, INCOMPLETE_EXCLUSION},
        )

    def update_model(self) -> None:
        self.model_obj.eligible = self.is_eligible
        self.model_obj.reasons_ineligible = self.reasons_ineligible

    def review_inclusion(self, reasons_ineligible: dict[str, str]) -> dict[str, str]:
        criteria = [
            getattr(self.model_obj, attr, None)
            for attr in [
                "willing_to_participate",
                "consent_ability",
                "hiv_pos",
                "cd4_date",
                "serum_crag_value",
                "serum_crag_date",
                "lp_done",
                "lp_declined",
                "csf_crag_value",
            ]
        ]
        if (
            not all(criteria)
            or NOT_EVALUATED in criteria
            or getattr(self.model_obj, "age_in_years", None) is None
            or getattr(self.model_obj, "cd4_value", None) is None
        ):
            reasons_ineligible.update(inclusion_criteria=INCOMPLETE_INCLUSION)
        if self.model_obj.willing_to_participate == NO:
            reasons_ineligible.update(willing_to_participate="Unwilling to participate")
        if self.model_obj.consent_ability == NO:
            reasons_ineligible.update(consent_ability="Incapable of consenting")
        if (
            self.model_obj.age_in_years is not None
            and self.model_obj.age_in_years < EIGHTEEN_YEARS
        ):
            reasons_ineligible.update(age_in_years="Age not >= 18")
        if self.model_obj.hiv_pos == NO:
            reasons_ineligible.update(hiv_pos="Not HIV sero-positive")
        reasons_ineligible = self.review_cd4(reasons_ineligible)
        reasons_ineligible = self.review_serum_crag(reasons_ineligible)
        return self.review_lp_csf_crag(reasons_ineligible)

    def review_cd4(self, reasons_ineligible: dict[str, str]) -> dict[str, str]:
        report_datetime = getattr(self.model_obj, "report_datetime", None)
        cd4_date = getattr(self.model_obj, "cd4_date", None)

        if self.model_obj.cd4_value is not None and self.model_obj.cd4_value >= ONE_HUNDRED:
            reasons_ineligible.update(cd4_value=f"CD4 not <100 {CELLS_PER_MICROLITER}")
        elif (
            report_datetime
            and cd4_date
            and abs((to_local(report_datetime).date() - cd4_date).days) > SIXTY_DAYS
        ):
            reasons_ineligible.update(cd4_date="CD4 > 60 days")
        return reasons_ineligible

    def review_serum_crag(self, reasons_ineligible: dict[str, str]) -> dict[str, str]:
        report_datetime = getattr(self.model_obj, "report_datetime", None)
        serum_crag_date = getattr(self.model_obj, "serum_crag_date", None)

        if self.model_obj.serum_crag_value != POS:
            reasons_ineligible.update(serum_crag_value="Serum CrAg not (+)")
        elif (
            report_datetime
            and serum_crag_date
            and abs((to_local(report_datetime).date() - serum_crag_date).days)
            > TWENTY_ONE_DAYS
        ):
            reasons_ineligible.update(serum_crag_date="Serum CrAg > 21 days")
        return reasons_ineligible

    def review_lp_csf_crag(self, reasons_ineligible: dict[str, str]) -> dict[str, str]:
        if self.model_obj.csf_crag_value == PENDING:
            reasons_ineligible.update(csf_crag_value=CSF_CRAG_PENDING)
        elif self.model_obj.csf_crag_value == POS:
            reasons_ineligible.update(csf_crag_value="CSF CrAg (+)")
        elif self.model_obj.csf_crag_value == NOT_DONE:
            reasons_ineligible.update(lp_done="LP done")
            reasons_ineligible.update(csf_crag_value="CSF CrAg not done")
        elif self.model_obj.lp_done == NO and self.model_obj.lp_declined != YES:
            reasons_ineligible.update(lp_done="LP not done")
            reasons_ineligible.update(lp_declined="LP not declined")
        return reasons_ineligible

    def review_exclusion(
        self,
        reasons_ineligible: dict[str, str],
    ) -> dict[str, str]:
        criteria = [
            getattr(self.model_obj, attr, None)
            for attr in [
                "pregnant",
                "breast_feeding",
                "prior_cm_episode",
                "reaction_to_study_drugs",
                "on_flucon",
                "contraindicated_meds",
                "mg_severe_headache",
                "mg_headache_nuchal_rigidity",
                "mg_headache_vomiting",
                "mg_seizures",
                "mg_gcs_lt_15",
                "any_other_mg_ssx",
                "jaundice",
                "cm_in_csf",
                "unsuitable_for_study",
            ]
        ]
        if not all(criteria) or NOT_EVALUATED in criteria:
            reasons_ineligible.update(exclusion_criteria=INCOMPLETE_EXCLUSION)
        if self.model_obj.contraindicated_meds == YES:
            reasons_ineligible.update(
                contraindicated_meds="Contraindicated concomitant medications",
            )
        if self.model_obj.cm_in_csf == YES:
            reasons_ineligible.update(cm_in_csf="Positive evidence of CM on CSF")
        if self.model_obj.jaundice == YES:
            reasons_ineligible.update(jaundice="Jaundice")
        if self.model_obj.on_flucon == YES:
            reasons_ineligible.update(on_flucon="On fluconazole")
        if self.model_obj.pregnant == YES:
            reasons_ineligible.update(pregnant="Pregnant")
        if self.model_obj.breast_feeding == YES:
            reasons_ineligible.update(breast_feeding="Breastfeeding")
        if self.model_obj.prior_cm_episode == YES:
            reasons_ineligible.update(prior_cm_episode="Prior episode of CM")
        if self.model_obj.reaction_to_study_drugs == YES:
            reasons_ineligible.update(
                reaction_to_study_drugs="Serious reaction to flucytosine or fluconazole",
            )
        reasons_ineligible = self.review_mg_ssx(reasons_ineligible)
        if self.model_obj.unsuitable_for_study == YES:
            reasons_ineligible.update(unsuitable_for_study="Deemed unsuitable other reason")

        return reasons_ineligible

    def review_mg_ssx(self: Any, reasons_ineligible: dict[str, str]) -> dict[str, str]:
        """Exclusion for clinical symptoms/signs of symptomatic meningitis."""
        for mg_ssx in [
            "mg_severe_headache",
            "mg_headache_nuchal_rigidity",
            "mg_headache_vomiting",
            "mg_seizures",
            "mg_gcs_lt_15",
            "any_other_mg_ssx",
        ]:
            if getattr(self.model_obj, mg_ssx, None) == YES:
                reasons_ineligible.update({mg_ssx: "Signs of symptomatic meningitis"})
        return reasons_ineligible

    @property
    def display_label(self) -> str:
        display_label = super().display_label
        if self.eligible == self.incomplete_value:
            display_label = self.incomplete_display_label
        return display_label
