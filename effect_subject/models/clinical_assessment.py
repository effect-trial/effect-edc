from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA, YES_NO_UNKNOWN
from edc_model import models as edc_models

from effect_lists.models import (
    ArvRegimens,
    NeurologicalConditions,
    SignificantNewDiagnoses,
    Symptoms,
    TbTreatments,
    XRayResults,
)

from ..choices import (
    ANTIBIOTIC_CHOICES,
    ASSESSMENT_METHODS,
    CLINICAL_ASSESSMENT_INFO_SOURCES,
    CM_TX_CHOICES,
    ECOG_SCORES,
    MODIFIED_RANKIN_SCORE_CHOICES,
    PATIENT_STATUSES,
    STEROID_CHOICES,
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

    date_of_death_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="If date of death provided, is this date estimated?"
    )

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
        # TODO - insert list/options for focal_neurologic_deficits?
        NeurologicalConditions,
        related_name="neurological_conditions",
        verbose_name="Does patient have any of the following neurological conditions?",
        blank=True,
    )

    focal_neurological_deficit_other = edc_models.OtherCharField()

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
        # TODO: If yes, prompt for SAE form
        choices=YES_NO,
        help_text="If yes, complete SAE report",
    )
    gi_side_effects = models.CharField(
        verbose_name="Has the patient experienced any gastrointestinal side effects?",
        # TODO: If yes, prompt for SAE form
        choices=YES_NO,
        help_text="If yes, complete SAE report",
    )
    gi_side_effects_details = models.TextField(
        verbose_name="If yes, please give details",
        null=True,
        blank=True,
    )

    any_significant_new_diagnoses = models.CharField(
        verbose_name="Other significant new diagnoses since last visit?",
        choices=YES_NO,
    )

    # TODO: ???If yes, date of diagnosis?

    significant_new_diagnoses = models.ManyToManyField(
        SignificantNewDiagnoses,
        verbose_name="Please select all new significant diagnoses that are relevant",
    )

    significant_new_diagnoses_other = edc_models.OtherCharField()

    chest_xray = models.CharField(
        verbose_name="Has a chest x-ray been carried out?",
        choices=YES_NO,
    )

    chest_xray_date = models.DateField(
        verbose_name="If yes, what date was it performed?",
        null=True,
        blank=True,
    )

    chest_xray_results = models.ManyToManyField(
        XRayResults,
        verbose_name="Chest x-ray result?",
        # TODO: ???Confirm all that apply
        null=True,
        blank=True,
    )

    # ART
    patient_taking_art = models.CharField(
        verbose_name="Is the patient currently taking ART?",
        choices=YES_NO,
    )

    patient_adherent = models.CharField(
        verbose_name="If yes, is the patient adherent?",
        choices=YES_NO_NA,
    )

    new_art_regimen = models.CharField(
        verbose_name="Has the patient started a new ART regimen since their last study assessment",
        choices=YES_NO_NA,
    )

    # TODO: rename attribute appropriately
    new_art_regimen_start_date = models.DateField(
        # TODO: ???Is this:
        #  Start date of most recent ART regimen?
        #  Start date of new ART regimen?
        # TODO: null = True??
        verbose_name="Start date of this ART regimen?"
    )

    art_regimen_rx = models.ForeignKey(
        ArvRegimens,
        on_delete=models.PROTECT,
        # TODO: Is this:
        #  Start date of most recent ART regimen?
        #  Start date of new ART regimen?
        # TODO: null = True??
        verbose_name="Which drugs were prescribed for this ART regimen?",
    )

    arvs_stopped_this_episode = models.CharField(
        verbose_name="ARVs stopped this clinical episode?",
        # TODO NA?
        choices=YES_NO,
    )

    # Patient treatment
    lp_completed = models.CharField(
        verbose_name="LP completed?",
        # TODO If yes, prompt for lab results
        choices=YES_NO,
        help_text="If yes, complete laboratory results",
    )

    cm_confirmed = models.CharField(
        verbose_name="Cryptococcal meningitis confirmed?",
        choices=YES_NO,
    )

    cm_tx_administered = models.CharField(
        verbose_name="Cryptococcal meningitis treatment administered?",
        choices=YES_NO,
    )

    cm_tx_given = models.CharField(
        verbose_name="Cryptococcal meningitis treatment given?",
        # TODO: ???>1 possible?
        choices=CM_TX_CHOICES,
    )

    cm_tx_given_other = edc_models.OtherCharField()

    tb_tx_given = models.ManyToManyField(
        TbTreatments,
        verbose_name="TB treatment given?",
        null=True,
        blank=True,
    )

    steroids_administered = models.CharField(
        verbose_name="Steroids administered?",
        choices=YES_NO,
    )

    which_steroids = models.CharField(
        verbose_name="If yes, which steroids where administered?",
        # TODO: ???>1 possible?
        choices=STEROID_CHOICES,
    )

    which_steroids_other = edc_models.OtherCharField()

    steroids_course_duration = models.IntegerField(
        verbose_name="Length of steroid course?",
        validators=[MinValueValidator(0)],
        help_text="in days",
    )

    co_trimoxazole = models.CharField(
        verbose_name="Co-Trimoxazole given?",
        choices=YES_NO,
    )

    antibiotics = models.CharField(
        verbose_name="Antibiotics?",
        # TODO: ???>1 possible?
        choices=ANTIBIOTIC_CHOICES,
    )

    # Treatment at day 14
    # TODO: Following section only available on day 14
    other_antibiotics_first_2w = models.CharField()
    # TODO: other_antibiotics_first_2w_other
    other_drugs_first_2w = models.CharField()
    # TODO: other_drugs_first_2w_other
    # TODO: other_interventions_first_2w_other
    medicines_rx_d14 = models.CharField()
    # TODO: medicines_rx_d14_other

    comments = models.TextField(
        # TODO: ???Every clinical assessment, or d14 only?
        verbose_name="Comments on Clinical care/Assessment/Plan:"
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Clinical Assessment"
        verbose_name_plural = "Clinical Assessment"
