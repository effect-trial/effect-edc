from edc_constants.constants import NEG, NO, NOT_ANSWERED, POS, YES
from edc_reportable import CELLS_PER_MICROLITER
from edc_screening.screening_eligibility import (
    ScreeningEligibility as BaseScreeningEligibility,
)


class ScreeningEligibility(BaseScreeningEligibility):
    def assess_eligibility(self):
        reasons_ineligible = {}
        reasons_ineligible.update(**self.review_inclusion(reasons_ineligible))
        reasons_ineligible.update(**self.review_exclusion(reasons_ineligible))
        self.eligible = NO if reasons_ineligible else YES
        self.reasons_ineligible = reasons_ineligible

    def update_model(self) -> None:
        self.model_obj.eligible = self.is_eligible
        self.model_obj.reasons_ineligible = self.reasons_ineligible

    def review_inclusion(self, reasons_ineligible: dict) -> dict:
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
        if not (all(criteria) and NOT_ANSWERED not in criteria):
            reasons_ineligible.update(
                inclusion_criteria="Incomplete inclusion criteria"
            )
        if self.model_obj.hiv_pos != YES:
            reasons_ineligible.update(hiv_pos="Not HIV sero-positive")
        if self.model_obj.cd4_value and self.model_obj.cd4_value >= 100:
            reasons_ineligible.update(cd4_value=f"CD4 not <100 {CELLS_PER_MICROLITER}")
        reasons_ineligible = self.review_crag(reasons_ineligible)
        return reasons_ineligible

    def review_crag(self, reasons_ineligible: dict) -> dict:
        if (
            self.model_obj.serum_crag_value == POS
            and self.model_obj.csf_crag_value == NEG
        ):
            pass
        elif self.model_obj.serum_crag_value != POS:
            reasons_ineligible.update(crag_value="Serum CrAg not (+)")
        elif (
            self.model_obj.serum_crag_value == POS
            and self.model_obj.csf_crag_value != NEG
        ):
            reasons_ineligible.update(crag_value="Serum CrAg(+) / CSF CrAg not (-)")
        return reasons_ineligible

    def review_exclusion(self, reasons_ineligible: dict) -> dict:
        criteria = [
            getattr(self.model_obj, attr, None)
            for attr in [
                "pregnant_or_bf",
                "prior_cm_epidose",
                "reaction_to_study_drugs",
                "on_fluconazole",
                "contraindicated_meds",
                "meningitis_symptoms",
                "jaundice",
                "csf_cm_evidence",
            ]
        ]
        if not (all(criteria) and NOT_ANSWERED not in criteria):
            reasons_ineligible.update(
                exclusion_criteria="Incomplete exclusion criteria"
            )
        if self.model_obj.contraindicated_meds not in [NO, NOT_ANSWERED]:
            reasons_ineligible.update(
                contraindicated_meds="Contraindicated concomitant medications"
            )
        if self.model_obj.csf_cm_evidence == YES:
            reasons_ineligible.update(csf_cm_evidence="Positive evidence of CM on CSF")
        if self.model_obj.jaundice not in [NO, NOT_ANSWERED]:
            reasons_ineligible.update(jaundice="Jaundice")
        if self.model_obj.meningitis_symptoms not in [NO, NOT_ANSWERED]:
            reasons_ineligible.update(
                meningitis_symptoms="Signs of symptomatic meningitis"
            )
        if self.model_obj.on_fluconazole not in [NO, NOT_ANSWERED]:
            reasons_ineligible.update(on_fluconazole="On fluconazole")
        if self.model_obj.pregnant_or_bf == YES:
            reasons_ineligible.update(pregnant_or_bf="Pregnant or breastfeeding")
        if self.model_obj.prior_cm_epidose not in [NO, NOT_ANSWERED]:
            reasons_ineligible.update(prior_cm_epidose="Prior episode of CM")
        if self.model_obj.reaction_to_study_drugs not in [NO, NOT_ANSWERED]:
            reasons_ineligible.update(
                reaction_to_study_drugs="Serious reaction to flucytosine or fluconazole"
            )
        return reasons_ineligible
