from django.db import models
from edc_constants.choices import POS_NEG_NOT_DONE, PREG_YES_NO_NA, YES_NO, YES_NO_TBD
from edc_constants.constants import QUESTION_RETIRED, TBD
from edc_model.models import BaseUuidModel
from edc_reportable import CELLS_PER_MICROLITER
from edc_screening.model_mixins import ScreeningModelMixin
from edc_screening.screening_identifier import (
    ScreeningIdentifier as BaseScreeningIdentifier,
)

from ..choices import CSF_RESULT, LP_STATUS


class SubjectScreeningModelError(Exception):
    pass


class ScreeningIdentifier(BaseScreeningIdentifier):

    template = "S{random_string}"


class SubjectScreening(
    ScreeningModelMixin,
    BaseUuidModel,
):

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
        verbose_name="Is the patient willing to participate in the study if found eligibel?",
        max_length=25,
        choices=YES_NO,
    )

    capable_to_consent = models.CharField(
        verbose_name="Does the patient have capacity to provide informed consent for participation?",
        max_length=25,
        choices=YES_NO,
    )

    hiv_pos = models.CharField(
        verbose_name="Is the patient HIV sero-positive", max_length=15, choices=YES_NO
    )

    cd4_value = models.IntegerField(
        verbose_name="CD4 count",
        help_text=CELLS_PER_MICROLITER,
    )

    cd4_date = models.DateField(
        verbose_name="CD4 count date",
    )

    pregnant_or_bf = models.CharField(
        verbose_name="Is the patient pregnant or breastfeeding?",
        max_length=15,
        choices=PREG_YES_NO_NA,
    )

    crag_value = models.CharField(
        verbose_name="Serum/plasma CrAg test result performed within the last 14 days",
        max_length=15,
        choices=POS_NEG_NOT_DONE,
        null=True,
        blank=False,
    )

    lp_status = models.CharField(
        verbose_name="Lumbar puncture:",
        max_length=15,
        choices=LP_STATUS,
        null=True,
        blank=False,
    )

    csf_crag_value = models.CharField(
        verbose_name="CSF CrAg result",
        max_length=15,
        choices=POS_NEG_NOT_DONE,
        null=True,
        blank=False,
    )

    prior_cm_epidose = models.CharField(
        verbose_name="Has the patient had a prior episode of CM?",
        max_length=25,
        choices=YES_NO,
    )

    prior_cm_epidose_date = models.DateField(
        verbose_name="CM episode date",
    )

    reaction_to_study_drugs = models.CharField(
        verbose_name="Has the patient had any serious reaction to flucytosine or fluconazole?",
        max_length=25,
        choices=YES_NO,
    )

    on_fluconazole = models.CharField(
        verbose_name=(
            "Is the patent already taking high-dose "
            "fluconazole treatment (800-1200 mg/day) for ≥1 week?"
        ),
        max_length=25,
        choices=YES_NO,
    )

    contraindicated_meds = models.CharField(
        verbose_name=(
            "Is the patient taking any contraindicated "
            "concomitant medications (see below)?"
        ),
        max_length=25,
        choices=YES_NO,
    )

    meningitis_symptoms = models.CharField(
        verbose_name=(
            "Has the patient had clinical symptoms/ signs of symptomatic "
            "meningitis at any time since CrAg screening?"
        ),
        max_length=25,
        choices=YES_NO,
        help_text=(
            "i.e. a progressively severe headache OR a headache and marked nuchal "
            "rigidity OR a head- ache and vomiting OR seizures OR a Glasgow "
            "Coma Scale (GCS) score of <15?"
        ),
    )

    jaundice = models.CharField(
        verbose_name="Based on clinical examination, does the patient have Jaundice?",
        max_length=25,
        choices=YES_NO,
    )

    # TODO: refers to question 15
    csf_value = models.CharField(
        verbose_name="CSF result for CM?",
        max_length=25,
        choices=CSF_RESULT,
        help_text=(
            "i.e. positive microscopy with India Ink, culture, or CrAg test) at any "
            "time between the CrAg test and screening for eligibility, or during the "
            "first 2 weeks of antifungal treatment, while the patient remained "
            "without clinical symptoms/ signs of meningitis as described in "
            "15 above (late withdrawal criterion)"
        ),
    )

    csf_date = models.DateField(
        verbose_name="CSF date",
        null=True,
    )

    eligible = models.CharField(
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
        editable=False,
        help_text="system calculated value",
    )

    reasons_ineligible = models.TextField(max_length=150, null=True, editable=False)

    def save(self, *args, **kwargs):
        if self._meta.label_lower == "meta_screening.subjectscreening":
            raise SubjectScreeningModelError(
                "Unable to save. Save via P1-3 proxy models."
            )
        self.consent_ability = QUESTION_RETIRED
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Subject Screening"
        verbose_name_plural = "Subject Screening"
