from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA, YES_NO_UNKNOWN
from edc_model import models as edc_models

from effect_lists.models import (
    Antibiotics,
    ArvRegimens,
    Drugs,
    FocalNeurologicDeficits,
    MedicinesRxDay14,
    SignificantNewDiagnoses,
    Symptoms,
    TbTreatments,
    XRayResults,
)

from ..choices import (
    ASSESSMENT_METHODS,
    CM_TX_CHOICES,
    ECOG_SCORES,
    MODIFIED_RANKIN_SCORE_CHOICES,
    PATIENT_STATUSES,
    SPOKE_TO_CHOICES,
    STEROID_CHOICES,
)
from ..model_mixins import CrfModelMixin, VitalsFieldsModelMixin


class ClinicalAssessment(
    VitalsFieldsModelMixin, CrfModelMixin, edc_models.BaseUuidModel
):

    # TODO: Schedule for d1 and d14

    # Initial Clinical Assessment CRF (p1)
    who_speak_to = models.CharField(
        verbose_name="Who did you speak to?",
        max_length=15,
        choices=SPOKE_TO_CHOICES,
    )

    who_speak_to_other = edc_models.OtherCharField()

    assessment_method = models.CharField(
        verbose_name="Was this a telephone follow up or an in person visit?",
        max_length=15,
        choices=ASSESSMENT_METHODS,
    )

    patient_hospitalized = models.CharField(
        verbose_name="Has the patient been hospitalized",
        max_length=15,
        # TODO: If yes, trigger SAE
        choices=YES_NO_NA,
    )

    patient_status = models.CharField(
        verbose_name="Patient status?",
        max_length=15,
        # TODO: Validate against visit survival status
        # TODO: If dead, trigger SAE -> death form -> off study
        choices=PATIENT_STATUSES,
    )

    adherence_counselling = models.CharField(
        verbose_name="Was adherence counselling given?",
        max_length=15,
        choices=YES_NO_NA,
    )

    cm_signs_symptoms = models.CharField(
        verbose_name=(
            "Has the patient had signs or symptoms of "
            "cryptococcal meningitis (CM) since last contact with trial team?"
        ),
        max_length=15,
        choices=YES_NO_UNKNOWN,
    )

    # Current Signs/Symptoms CRF (p2)
    current_symptoms = models.ManyToManyField(
        Symptoms,
        related_name="current_symptoms",
        verbose_name="Is patient currently experiencing any of the following signs/symptoms?",
        blank=True,
    )

    headache_duration = models.IntegerField(
        # TODO: Only valid if headache selected in current_symptoms
        verbose_name="If patient currently has headache, for what duration have they had it for",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="in days",
    )

    # Current Signs/Symptoms - Neurological Questions CRF (p2)
    meningism = models.CharField(
        verbose_name="Meningism?",
        max_length=15,
        choices=YES_NO,
    )

    papilloedema = models.CharField(
        verbose_name="Papilloedema?",
        max_length=15,
        choices=YES_NO,
    )

    focal_neurologic_deficits = models.ManyToManyField(
        FocalNeurologicDeficits,
        related_name="focal_neurologic_deficits",
        verbose_name="Does patient have any of the following focal neurologic deficits?",
        blank=True,
    )

    cn_palsy_left_other = edc_models.OtherCharField(
        verbose_name="If other cranial nerve palsy (left), please specify ..."
    )

    cn_palsy_right_other = edc_models.OtherCharField(
        verbose_name="If other cranial nerve palsy (right), please specify ..."
    )

    focal_neurologic_deficits_other = edc_models.OtherCharField(
        verbose_name="If other focal neurologic deficit, please specify ..."
    )

    visual_field_loss = models.TextField(
        # TODO: ???Link to visual_field_disturbance focal_neurologic_deficits field?
        verbose_name="If visual field loss, please provide details ...",
        null=True,
    )

    # Current Signs/Symptoms - Mental Status CRF (p2)
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

    ecog_score = models.CharField(
        verbose_name="ECOG score?",
        max_length=15,
        choices=ECOG_SCORES,
    )

    # See: https://www.ncbi.nlm.nih.gov/books/NBK513298/#article-22258.s3
    glasgow_coma_score = models.IntegerField(
        verbose_name="Glasgow Coma Score?",
        validators=[MinValueValidator(3), MaxValueValidator(15)],
        help_text="/15",
    )

    # Vital Signs CRF (p2)
    # vitals_fields_model_mixin configured for vitals
    # TODO: Move TemperatureField to core edc(-vitals)
    # TODO: ???Implement RespiratoryRateField and HeartRateField?

    # Current Signs/Symptoms - Other CRF (p2)
    patient_admitted = models.CharField(
        verbose_name="Has the patient been admitted due to these symptoms?",
        # TODO: If yes, prompt for SAE form
        choices=YES_NO,
        help_text="If yes, complete SAE report",
    )

    symptoms_gte_g3 = models.CharField(
        verbose_name="Are any of these symptoms Grade 3 or above?",
        max_length=15,
        # TODO: If yes, prompt for SAE
        choices=YES_NO_NA,
    )

    # Diagnoses CRF (p3)
    gi_side_effects = models.CharField(
        verbose_name="Has the patient experienced any gastrointestinal side effects?",
        # TODO: If yes, prompt for SAE form (where appropriate???)
        choices=YES_NO,
        help_text="If yes, complete SAE report where appropriate",
    )

    gi_side_effects_details = models.TextField(
        verbose_name="If yes, please give details",
        null=True,
        blank=True,
    )

    any_significant_new_diagnoses = models.CharField(
        # TODO: determine and display date of last visit
        verbose_name="Other significant new diagnoses since last visit?",
        choices=YES_NO,
    )

    # TODO: ???If yes, date of diagnosis?
    # TODO: Request to handle one date per diagnosis

    # Significant Diagnoses CRF (p3)
    significant_new_diagnoses = models.ManyToManyField(
        SignificantNewDiagnoses,
        verbose_name="Please select all new significant diagnoses that are relevant",
    )

    significant_new_diagnoses_other = edc_models.OtherCharField()

    # Chest X-ray CRF (p3)
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
        null=True,
        blank=True,
    )

    # ART / ARV CRF (p3)
    patient_taking_art = models.CharField(
        verbose_name="Is the patient currently taking ART?",
        choices=YES_NO,
    )

    patient_adherent = models.CharField(
        verbose_name="If yes, is the patient adherent?",
        choices=YES_NO_NA,
    )

    new_art_regimen = models.CharField(
        # TODO: determine and display date of last study assessment
        verbose_name="Has the patient started a new ART regimen since their last study assessment",
        choices=YES_NO_NA,
    )

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
        # TODO: Clarify when this question is required (d1, d14),
        #  and/or in response to “decision made re ART?” e.g. stopped, continued etc
        # TODO: null = True??
        verbose_name="Which drugs were prescribed for this ART regimen?",
    )

    arvs_stopped_this_episode = models.CharField(
        verbose_name="ARVs stopped this clinical episode?",
        # TODO: YES_NO_NA?
        choices=YES_NO,
    )

    # Patient Treatment CRF (p4)
    lp_completed = models.CharField(
        verbose_name="LP completed?",
        # TODO: If yes, prompt for lab results
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
        choices=CM_TX_CHOICES,
    )

    cm_tx_given_other = edc_models.OtherCharField()

    tb_tx_given = models.ManyToManyField(
        TbTreatments,
        verbose_name="TB treatment given?",
        null=True,
    )

    steroids_administered = models.CharField(
        verbose_name="Steroids administered?",
        choices=YES_NO,
    )

    which_steroids = models.CharField(
        verbose_name="If yes, which steroids where administered?",
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

    # TODO: ???d1 only?
    antibiotics = models.ManyToManyField(
        Antibiotics,
        verbose_name="Antibiotics?",
        null=True,
    )

    # Treatment at day 14
    # TODO: Following section only available on day 14
    other_antibiotics_first_2w = models.ManyToManyField(
        Antibiotics,
        verbose_name="Other antibiotics given during the first 14 days?",
        null=True,
    )
    other_antibiotics_first_2w_other = edc_models.OtherCharField()

    other_drugs_first_2w = models.ManyToManyField(
        Drugs,
        verbose_name="Other drugs/intervention given during the first 14 days?",
        null=True,
    )
    other_drugs_first_2w_other = edc_models.OtherCharField()

    medicines_rx_d14 = models.ManyToManyField(
        MedicinesRxDay14,
        verbose_name="Medicines prescribed on day 14?",
        null=True,
    )
    medicines_rx_d14_other = edc_models.OtherCharField()

    # Clinical Notes CRF (p5)
    # TODO: Ask on every visit
    comments = models.TextField(
        verbose_name="Comments on Clinical care/Assessment/Plan:"
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Clinical Assessment"
        verbose_name_plural = "Clinical Assessment"
