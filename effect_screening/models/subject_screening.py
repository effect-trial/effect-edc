from django.core.validators import MinValueValidator
from django.db import models
from django.utils.html import format_html
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_ANSWERED, NOT_APPLICABLE
from edc_model.models import BaseUuidModel, date_not_future
from edc_reportable import CELLS_PER_MICROLITER
from edc_screening.model_mixins import EligibilityModelMixin, ScreeningModelMixin
from edc_screening.screening_identifier import (
    ScreeningIdentifier as BaseScreeningIdentifier,
)

from ..choices import (
    CSF_YES_NO_PENDING_NA,
    POS_NEG_IND_NOT_ANSWERED,
    POS_NEG_IND_PENDING_NA,
    PREG_YES_NO_NA_NOT_ANSWERED,
    YES_NO_NOT_ANSWERED,
)
from ..eligibility import ScreeningEligibility


class ScreeningIdentifier(BaseScreeningIdentifier):

    template = "S{random_string}"


class SubjectScreening(
    ScreeningModelMixin,
    EligibilityModelMixin,
    BaseUuidModel,
):

    eligibility_cls = ScreeningEligibility

    identifier_cls = ScreeningIdentifier

    screening_consent = models.CharField(
        verbose_name=(
            "Has the subject given his/her verbal consent "
            "to be screened for the EFFECT trial?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    willing_to_participate = models.CharField(
        verbose_name="Is the patient willing to participate in the study if found eligible?",
        max_length=25,
        choices=YES_NO,
    )

    consent_ability = models.CharField(
        verbose_name=(
            "Does the patient have capacity to provide informed consent for participation?"
        ),
        max_length=25,
        choices=YES_NO,
    )

    hiv_pos = models.CharField(
        verbose_name="Is the patient HIV sero-positive",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    cd4_value = models.IntegerField(
        verbose_name="Most recent CD4 count",
        validators=[MinValueValidator(0)],
        null=True,
        blank=False,
        help_text=f"Eligible if CD4 count <100 {CELLS_PER_MICROLITER}",
    )

    cd4_date = models.DateField(
        verbose_name="Most recent CD4 count sample collection date",
        validators=[date_not_future],
        null=True,
        blank=False,
    )

    pregnant_or_bf = models.CharField(
        verbose_name="Is the patient pregnant or breastfeeding?",
        max_length=15,
        choices=PREG_YES_NO_NA_NOT_ANSWERED,
        default=NOT_ANSWERED,
        blank=False,
    )

    # eligible if POS
    serum_crag_value = models.CharField(
        verbose_name="Serum/plasma CrAg result",
        max_length=15,
        choices=POS_NEG_IND_NOT_ANSWERED,
        default=NOT_ANSWERED,
        blank=False,
    )

    serum_crag_date = models.DateField(
        verbose_name="Date of serum/plasma CrAg result",
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text="Test must have been performed within the last 14 days",
    )

    lp_done = models.CharField(
        verbose_name="Was LP done?",
        max_length=15,
        choices=YES_NO_NOT_ANSWERED,
        default=NOT_ANSWERED,
        null=True,
        blank=False,
        help_text="If YES, provide date below",
    )

    lp_date = models.DateField(
        verbose_name="LP date",
        null=True,
        blank=True,
        help_text="LP date must be after AFTER serum/plasma CrAg result",
    )

    lp_declined = models.CharField(
        verbose_name="If LP not done, was LP declined?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        blank=False,
    )

    csf_crag_value = models.CharField(
        verbose_name="CSF CrAg result",
        max_length=15,
        choices=POS_NEG_IND_PENDING_NA,
        default=NOT_APPLICABLE,
        blank=False,
        help_text=(
            "If result is `pending`, report on DAY 1 / baseline visit or when available."
        ),
    )

    prior_cm_epidose = models.CharField(
        verbose_name="Has the patient had a prior episode of CM?",
        max_length=25,
        choices=YES_NO_NOT_ANSWERED,
        default=NOT_ANSWERED,
        blank=False,
    )

    reaction_to_study_drugs = models.CharField(
        verbose_name="Has the patient had any serious reaction to flucytosine or fluconazole?",
        max_length=25,
        choices=YES_NO_NOT_ANSWERED,
        default=NOT_ANSWERED,
        blank=False,
    )

    # exclusion
    on_fluconazole = models.CharField(
        verbose_name=(
            "Has the patient taken 7 or more doses of high-dose fluconazole "
            "treatment in the last 7 days?"
        ),
        max_length=25,
        choices=YES_NO_NOT_ANSWERED,
        default=NOT_ANSWERED,
        blank=False,
        help_text="fluconazole @ (800-1200 mg/day)",
    )

    # exclusion
    contraindicated_meds = models.CharField(
        verbose_name=(
            "Is the patient taking any contraindicated " "concomitant medications?"
        ),
        max_length=25,
        choices=YES_NO_NOT_ANSWERED,
        default=NOT_ANSWERED,
        blank=False,
        help_text="Refer to the protocol for a complete list",
    )

    # exclusion
    meningitis_symptoms = models.CharField(
        verbose_name=(
            "Has the patient had clinical symptoms/ signs of symptomatic "
            "meningitis at any time since CrAg screening?"
        ),
        max_length=25,
        choices=YES_NO_NOT_ANSWERED,
        default=NOT_ANSWERED,
        blank=False,
    )

    # exclusion
    jaundice = models.CharField(
        verbose_name="Based on clinical examination, does the patient have jaundice?",
        max_length=25,
        choices=YES_NO_NOT_ANSWERED,
        default=NOT_ANSWERED,
        blank=False,
    )

    # TODO: If pending, get at baseline
    csf_cm_evidence = models.CharField(
        verbose_name="Any other evidence of CM on CSF?",
        max_length=25,
        choices=CSF_YES_NO_PENDING_NA,
        default=NOT_APPLICABLE,
        blank=False,
        help_text=format_html(
            "At any time between the CrAg test and screening for eligibility. "
            "<BR>If results on tests on CSF are `pending`, report on "
            "DAY 1 / baseline visit or when available.",
        ),
    )

    csf_results_date = models.DateField(
        verbose_name="Date `pending results` expected (estimate)", null=True, blank=True
    )

    class Meta:
        verbose_name = "Subject Screening"
        verbose_name_plural = "Subject Screening"
