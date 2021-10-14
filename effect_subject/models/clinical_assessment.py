from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA, YES_NO_UNKNOWN
from edc_model import models as edc_models

from effect_lists.models import NeurologicalConditions, Symptoms

from ..choices import (
    ASSESSMENT_METHODS,
    CLINICAL_ASSESSMENT_INFO_SOURCES,
    ECOG_SCORES,
    MODIFIED_RANKIN_SCORE_CHOICES,
    PATIENT_STATUSES,
)
from ..model_mixins import CrfModelMixin, VitalsFieldsModelMixin


class ClinicalAssessment(
    VitalsFieldsModelMixin, CrfModelMixin, edc_models.BaseUuidModel
):

    # TODO: Visit (e.g. d1, d3, ..., m4, m6, unscheduled) - is already stored, but do we need to display it?

    info_source = models.CharField(
        verbose_name="Who did you speak to?",
        max_length=15,
        choices=CLINICAL_ASSESSMENT_INFO_SOURCES,
    )

    assessment_method = models.CharField(
        verbose_name="Was this a telephone follow up or an in person visit?",
        max_length=15,
        choices=ASSESSMENT_METHODS,
    )

    adherence_counselling = models.CharField(
        verbose_name="Was adherence counselling given?",
        max_length=15,
        choices=YES_NO,
    )

    patient_status = models.CharField(
        verbose_name="Patient status?",
        max_length=15,
        # TODO: If dead, prompt for death & SAE form
        choices=PATIENT_STATUSES,
    )

    date_of_death_known = models.CharField(
        verbose_name="Is the date of death known?",
        max_length=15,
        choices=YES_NO,
    )

    date_of_death = models.DateField(
        verbose_name="Date of death",
        validators=[edc_models.date_not_future],
    )

    # TODO: Is this date estimated?
    # No
    # Yes, estimated the day
    # Yes, estimated the day and month

    cm_signs_symptoms = models.CharField(
        verbose_name=(
            "Has the patient had signs or symptoms of "
            "cryptococcal meningitis (CM) since last contact with trial team?"
        ),
        max_length=15,
        choices=YES_NO_UNKNOWN,
    )

    # Current signs/symptoms questions
    current_symptoms = models.ManyToManyField(
        Symptoms,
        related_name="current_symptoms",
        verbose_name="Is patient currently experiencing any of the following signs/symptoms?",
        blank=True,
    )

    headache_duration = models.IntegerField(
        verbose_name="If patient currently has headache, for what duration have they had it for",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="in days",
    )

    # Neurological questions
    neurological_symptoms = models.ManyToManyField(
        NeurologicalConditions,
        related_name="neurological_conditions",
        verbose_name="Does patient have any of the following neurological conditions?",
        blank=True,
    )

    # TODO - do we want to provide list/options for focal_neurologic_deficit_specify?
    # focal_neurological_deficit =

    cranial_nerve_palsy_other = edc_models.OtherCharField()

    # Mental status
    recent_seizure = models.CharField(
        verbose_name="Recent seizure (<72 hours)?",
        max_length=15,
        choices=YES_NO,
    )

    behaviour_change = models.CharField(
        verbose_name="Behaviour change?",
        max_length=15,
        choices=YES_NO,
    )

    confusion = models.CharField(
        verbose_name="Confusion?",
        max_length=15,
        choices=YES_NO,
    )

    modified_rankin_score = models.CharField(
        verbose_name="Modified Rankin Score?",
        max_length=15,
        choices=MODIFIED_RANKIN_SCORE_CHOICES,
    )

    # TODO: Add descriptions to choices
    ecog_score = models.CharField(
        verbose_name="ECOG score?",
        max_length=15,
        choices=ECOG_SCORES,
    )

    # See: https://www.ncbi.nlm.nih.gov/books/NBK513298/#article-22258.s3
    glasgow_coma_score = models.IntegerField(
        verbose_name="Glasgow Coma Score?",
        validators=[MinValueValidator(3), MaxValueValidator(15)],
    )

    # Other
    patient_admitted = models.CharField(
        verbose_name="Has the patient been admitted due to these symptoms?",
        # TODO: If yes, complete SAE report
        choices=YES_NO,
    )
    gi_side_effects = models.CharField(
        verbose_name="Has the patient experienced any gastrointestinal side effects?",
        choices=YES_NO,
    )
    gi_side_effects_details = models.TextField(
        verbose_name="If yes, please give details",
        null=True,
        blank=True,
    )

    # TODO: Is this necessary? Do/can we trigger from here?
    ae_report_required = models.TextField(
        verbose_name=(
            "If gastrointestinal side effects experienced, "
            "is an adverse event report required?"
        ),
        choices=YES_NO_NA,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Clinical Assessment"
        verbose_name_plural = "Clinical Assessment"
