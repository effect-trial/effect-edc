from edc_constants.constants import (
    NEG,
    NO,
    NOT_ANSWERED,
    NOT_APPLICABLE,
    PENDING,
    POS,
    YES,
)
from edc_reportable import CELLS_PER_MICROLITER
from edc_screening.screening_eligibility import FC
from edc_screening.screening_eligibility import (
    ScreeningEligibility as BaseScreeningEligibility,
)


class ScreeningEligibility(BaseScreeningEligibility):
    def __init__(self, **kwargs):
        self.age_in_years = None
        self.cd4_date = None
        self.cd4_value = None
        self.consent_ability = None
        self.contraindicated_meds = None
        self.csf_cm_evidence = None
        self.csf_crag_value = None
        self.csf_results_date = None
        self.hiv_pos = None
        self.jaundice = None
        self.lp_date = None
        self.lp_declined = None
        self.lp_done = None
        self.meningitis_symptoms = None
        self.on_fluconazole = None
        self.pregnant_or_bf = None
        self.prior_cm_epidose = None
        self.reaction_to_study_drugs = None
        self.report_datetime = None
        self.serum_crag_date = None
        self.serum_crag_value = None
        self.willing_to_participate = None
        super().__init__(**kwargs)

    def get_required_fields(self) -> dict[str, FC]:
        # inclusion
        required_fields = {
            "age_in_years": FC(range(18, 120), "<18 years old"),
            "willing_to_participate": FC(YES, "Unwilling to participate"),
            "consent_ability": FC(YES, "Incapable of consenting"),
            "hiv_pos": FC(YES, "Not HIV sero-positive"),
            "cd4_value": FC(range(0, 100), f"CD4 not <100 {CELLS_PER_MICROLITER}"),
            "cd4_date": FC(),
            "serum_crag_value": FC(
                POS, "Serum CrAg not POS", missing_value=NOT_ANSWERED
            ),
            "serum_crag_date": FC(),
            "lp_done": FC(
                [YES, NO, PENDING], "Was LP done?", missing_value=NOT_ANSWERED
            ),
            "lp_declined": FC([YES, NO, NOT_APPLICABLE]),
            "csf_crag_value": FC(
                [NEG, PENDING, NOT_APPLICABLE], "CSF CrAg not NEG/PENDING"
            ),
        }
        # exclusion
        required_fields.update(
            {
                "pregnant_or_bf": FC(
                    [NO, NOT_APPLICABLE],
                    "Pregnant or breastfeeding",
                    missing_value=NOT_ANSWERED,
                ),
                "prior_cm_epidose": FC(
                    NO, "Prior episode of CM", missing_value=NOT_ANSWERED
                ),
                "reaction_to_study_drugs": FC(
                    NO,
                    "Serious reaction to flucytosine or fluconazole",
                    missing_value=NOT_ANSWERED,
                ),
                "on_fluconazole": FC(NO, "On fluconazole", missing_value=NOT_ANSWERED),
                "contraindicated_meds": FC(
                    NO,
                    "Contraindicated concomitant medications",
                    missing_value=NOT_ANSWERED,
                ),
                "meningitis_symptoms": FC(
                    NO, "Signs of symptomatic meningitis", missing_value=NOT_ANSWERED
                ),
                "jaundice": FC(NO, "Jaundice", missing_value=NOT_ANSWERED),
                "csf_cm_evidence": FC(
                    NO, "Positive evidence of CM on CSF", missing_value=NOT_ANSWERED
                ),
            }
        )
        return required_fields

    def assess_eligibility(self):
        self.assess_cd4()
        self.assess_serum_crag()
        self.assess_serum_crag_and_csf()
        self.assess_csf()

    def assess_cd4(self):
        if self.cd4_date and self.report_datetime:
            if (self.report_datetime.date() - self.cd4_date).days > 21:
                self.reasons_ineligible.update(
                    cd4_date="CD4 21 days before report date"
                )
                self.eligible = NO

    def assess_serum_crag(self):
        """Assert serum CrAg date is not before CD4 date and
        is within 21 days of CD4.
        """
        if self.serum_crag_date and self.cd4_date:
            days = (self.cd4_date - self.serum_crag_date).days
            if days > 0:
                self.reasons_ineligible.update(serum_crag_date="Serum CrAg before CD4")
                self.eligible = NO
            if not 0 <= abs(days) <= 21:
                self.reasons_ineligible.update(
                    serum_crag_date="Serum CrAg not within 21 days of CD4"
                )
                self.eligible = NO
        if self.lp_date and self.lp_date < self.serum_crag_date:
            self.reasons_ineligible.update(lp_date="LP before serum CrAg")
            self.eligible = NO

    def assess_serum_crag_and_csf(self):
        if self.serum_crag_value == POS and self.csf_crag_value == NEG:
            pass
        elif self.serum_crag_value != POS:
            self.reasons_ineligible.update(crag_value="Serum CrAg not (+)")
            self.eligible = NO
        elif self.serum_crag_value == POS and self.csf_crag_value != NEG:
            self.reasons_ineligible.update(
                crag_value="Serum CrAg(+) / CSF CrAg not (-)"
            )
            self.eligible = NO

    def assess_csf(self):
        if (
            self.csf_results_date
            and self.lp_date
            and (self.lp_date > self.csf_results_date)
        ):
            self.reasons_ineligible.update(csf_results_date="CSF before LP")
            self.eligible = NO
        # TODO: not sure about CSF CrAg value and LP.
        #  In protocol says "CSF CrAg test negative or LP not done (declined)" ??
