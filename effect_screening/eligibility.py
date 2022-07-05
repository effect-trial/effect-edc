from typing import Any

from edc_constants.constants import IND, NO, PENDING, POS, TBD, YES
from edc_reportable import CELLS_PER_MICROLITER
from edc_screening.screening_eligibility import (
    ScreeningEligibility as BaseScreeningEligibility,
)


class ScreeningEligibility(BaseScreeningEligibility):
    eligible_values_list: list = [YES, NO, TBD, PENDING]

    def assess_eligibility(self: Any) -> None:
        reasons_ineligible = {}
        reasons_ineligible.update(**self.review_inclusion(reasons_ineligible))
        reasons_ineligible.update(**self.review_exclusion(reasons_ineligible))
        if self.model_obj.csf_crag_value == PENDING:
            self.eligible = PENDING
        else:
            self.eligible = (
                self.is_ineligible_value if reasons_ineligible else self.is_eligible_value
            )
        self.reasons_ineligible = reasons_ineligible

    def update_model(self: Any) -> None:
        self.model_obj.eligible = self.is_eligible
        self.model_obj.reasons_ineligible = self.reasons_ineligible

    def review_inclusion(self: Any, reasons_ineligible: dict) -> dict:
        if self.model_obj.willing_to_participate != YES:
            reasons_ineligible.update(willing_to_participate="Unwilling to participate")
        if self.model_obj.consent_ability != YES:
            reasons_ineligible.update(consent_ability="Incapable of consenting")
        criteria = [
            getattr(self.model_obj, attr, None)
            for attr in [
                "hiv_pos",
                "cd4_value",
                "cd4_date",
                "serum_crag_value",
                "serum_crag_date",
                "lp_done",
                "lp_declined",
                "csf_crag_value",
            ]
        ]
        if not all(criteria):
            reasons_ineligible.update(inclusion_criteria="Incomplete inclusion criteria")
        if self.model_obj.hiv_pos != YES:
            reasons_ineligible.update(hiv_pos="Not HIV sero-positive")
        if self.model_obj.cd4_value and self.model_obj.cd4_value >= 100:
            reasons_ineligible.update(cd4_value=f"CD4 not <100 {CELLS_PER_MICROLITER}")
        reasons_ineligible = self.review_crag(reasons_ineligible)
        return reasons_ineligible

    def review_crag(self: Any, reasons_ineligible: dict) -> dict:
        if self.model_obj.serum_crag_value != POS:
            reasons_ineligible.update(serum_crag_value="Serum CrAg not (+)")
        elif self.model_obj.serum_crag_value == POS:
            if self.model_obj.csf_crag_value == PENDING:
                reasons_ineligible.update(csf_crag_value="CSF CrAg pending")
            elif self.model_obj.csf_crag_value == POS:
                reasons_ineligible.update(csf_crag_value="CSF CrAg (+)")
            elif self.model_obj.csf_crag_value == IND:
                reasons_ineligible.update(csf_crag_value="CSF CrAg (IND)")
            elif self.model_obj.lp_done == NO and self.model_obj.lp_declined == NO:
                reasons_ineligible.update(lp_done="LP not done")
                reasons_ineligible.update(lp_declined="LP not declined")
        return reasons_ineligible

    def review_exclusion(self: Any, reasons_ineligible: dict) -> dict:
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
            ]
        ]
        if not all(criteria):
            reasons_ineligible.update(exclusion_criteria="Incomplete exclusion criteria")
        if self.model_obj.contraindicated_meds == YES:
            reasons_ineligible.update(
                contraindicated_meds="Contraindicated concomitant medications"
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
                reaction_to_study_drugs="Serious reaction to flucytosine or fluconazole"
            )
        reasons_ineligible = self.review_mg_ssx(reasons_ineligible)
        return reasons_ineligible

    def review_mg_ssx(self: Any, reasons_ineligible: dict) -> dict:
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
