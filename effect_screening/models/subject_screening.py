from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import PREG_YES_NO_NA_NOT_EVALUATED, YES_NO, YES_NO_NA
from edc_constants.constants import NOT_ANSWERED, NOT_APPLICABLE, NOT_EVALUATED, TBD
from edc_model.models import BaseUuidModel, date_not_future
from edc_reportable import CELLS_PER_MICROLITER
from edc_screening.model_mixins import EligibilityModelMixin, ScreeningModelMixin
from edc_screening.screening_identifier import (
    ScreeningIdentifier as BaseScreeningIdentifier,
)

from ..choices import (
    CSF_CM_RESULT,
    POS_NEG_IND_NOT_ANSWERED,
    POS_NEG_IND_PENDING_NA,
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

    willing_to_participate = models.CharField(
        verbose_name="Is the patient willing to participate in the study if found eligible?",
        max_length=25,
        choices=YES_NO,
    )

    consent_ability = models.CharField(
        verbose_name="Does the patient have capacity to provide informed consent for participation?",
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
        verbose_name="Most recent CD4 count date",
        validators=[date_not_future],
        null=True,
        blank=False,
    )

    pregnant_or_bf = models.CharField(
        verbose_name="Is the patient pregnant or breastfeeding?",
        max_length=15,
        choices=PREG_YES_NO_NA_NOT_EVALUATED,
        default=NOT_EVALUATED,
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
        choices=YES_NO,
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
        help_text="If result is `pending`, report on DAY 1 / baseline visit or when available.",
    )

    prior_cm_epidose = models.CharField(
        verbose_name="Has the patient had a prior episode of CM?",
        max_length=25,
        choices=YES_NO_NOT_ANSWERED,
        default=NOT_ANSWERED,
        blank=False,
    )

    # TODO: why is this here???
    prior_cm_epidose_date = models.DateField(
        verbose_name="CM episode date", null=True, blank=True
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
        verbose_name="Is the patent already taking high-dose fluconazole treatment?",
        max_length=25,
        choices=YES_NO_NOT_ANSWERED,
        default=NOT_ANSWERED,
        blank=False,
        help_text="fluconazole @ (800-1200 mg/day) for ≥1 week",
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
        help_text=(
            "i.e. a progressively severe headache OR a headache and marked nuchal "
            "rigidity OR a head- ache and vomiting OR seizures OR a Glasgow "
            "Coma Scale (GCS) score of <15?"
        ),
    )

    # exclusion
    jaundice = models.CharField(
        verbose_name="Based on clinical examination, does the patient have jaundice?",
        max_length=25,
        choices=YES_NO_NOT_ANSWERED,
        default=NOT_ANSWERED,
        blank=False,
    )

    # TODO: refers to question 15
    csf_cm_value = models.CharField(
        verbose_name="CSF result for CM?",
        max_length=25,
        choices=CSF_CM_RESULT,
        default=NOT_ANSWERED,
        blank=False,
        help_text=(
            "i.e. positive microscopy with India Ink, culture, or CrAg test) at any "
            "time between the CrAg test and screening for eligibility, or during the "
            "first 2 weeks of antifungal treatment, while the patient remained "
            "without clinical symptoms/ signs of meningitis as described in "
            "15 above (late withdrawal criterion)"
        ),
    )

    csf_cm_date = models.DateField(
        verbose_name="CSF date",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Subject Screening"
        verbose_name_plural = "Subject Screening"
