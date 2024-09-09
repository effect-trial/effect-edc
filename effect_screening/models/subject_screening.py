from django.contrib.sites.models import Site
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.html import format_html
from edc_constants.choices import (
    YES_NO,
    YES_NO_NA,
    YES_NO_NOT_EVALUATED,
    YES_NO_NOT_EVALUATED_NA,
)
from edc_constants.constants import NOT_APPLICABLE, NOT_EVALUATED, QUESTION_RETIRED
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future
from edc_model_fields.fields import OtherCharField
from edc_reportable import CELLS_PER_MICROLITER
from edc_screening.model_mixins import EligibilityModelMixin, ScreeningModelMixin
from edc_screening.screening_identifier import (
    ScreeningIdentifier as BaseScreeningIdentifier,
)

from effect_consent.consents import consent_v1, consent_v2

from ..choices import (
    CM_ON_CSF_METHODS,
    CSF_CRAG_RESULT_CHOICES,
    CSF_YES_NO_PENDING_NA,
    HIV_CONFIRMATION_METHODS,
    POS_NEG,
    PREG_YES_NO_NOT_EVALUATED_NA,
    UNSUITABLE_REASONS,
)
from ..eligibility import ScreeningEligibility


class ScreeningIdentifier(BaseScreeningIdentifier):
    template = "S{random_string}"


class SubjectScreening(ScreeningModelMixin, EligibilityModelMixin, BaseUuidModel):
    eligibility_cls = ScreeningEligibility

    identifier_cls = ScreeningIdentifier

    consent_definitions = [consent_v1, consent_v2]

    site = models.ForeignKey(Site, on_delete=models.PROTECT, null=True, related_name="+")

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
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
    )

    consent_ability = models.CharField(
        verbose_name=(
            "Does the patient have capacity to provide informed consent for participation?"
        ),
        max_length=25,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
    )

    parent_guardian_consent = models.CharField(
        verbose_name=(
            "If patient is under 18, do you have consent from "
            "the parent or legal guardian to capture this information?"
        ),
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="( if 'No', STOP )",
    )

    hiv_pos = models.CharField(
        verbose_name="Is the patient CONFIRMED HIV sero-positive?",
        max_length=15,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
        null=True,
        blank=False,
    )

    hiv_confirmed_date = models.DateField(
        verbose_name="If YES, on what date was HIV positivity confirmed?",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    hiv_confirmed_method = models.CharField(
        verbose_name="If YES, method?",
        max_length=50,
        choices=HIV_CONFIRMATION_METHODS,
        default=NOT_APPLICABLE,
    )

    cd4_value = models.IntegerField(
        verbose_name="Most recent CD4 count",
        validators=[MinValueValidator(0), MaxValueValidator(99)],
        null=True,
        blank=False,
        help_text=f"Eligible if CD4 count <100 {CELLS_PER_MICROLITER}.",
    )

    cd4_date = models.DateField(
        verbose_name="Most recent CD4 count sample collection date",
        validators=[date_not_future],
        null=True,
        blank=False,
    )

    # ineligible if YES
    pregnant = models.CharField(
        verbose_name="Is the patient pregnant?",
        max_length=15,
        choices=PREG_YES_NO_NOT_EVALUATED_NA,
        default=NOT_APPLICABLE,
    )

    preg_test_date = models.DateField(
        verbose_name="Pregnancy test date (Urine or serum βhCG)",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    # ineligible if YES
    breast_feeding = models.CharField(
        verbose_name="Is the patient breastfeeding?",
        max_length=15,
        choices=YES_NO_NOT_EVALUATED_NA,
        default=NOT_APPLICABLE,
    )

    # eligible if POS
    serum_crag_value = models.CharField(
        verbose_name="Serum/plasma CrAg result",
        max_length=15,
        choices=POS_NEG,
        blank=False,
    )

    serum_crag_date = models.DateField(
        verbose_name="Serum/plasma CrAg sample collection date",
        validators=[date_not_future],
        null=True,
        blank=False,
        help_text="Test must have been performed within the last 21 days.",
    )

    lp_done = models.CharField(
        verbose_name="Was LP done?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
        help_text="If YES, provide date below ...",
    )

    lp_date = models.DateField(
        verbose_name="LP date",
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text=(
            "LP should be done AFTER serum/plasma CrAg, "
            "but may be done no more than 3 days before the serum/plasma CrAg."
        ),
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
        choices=CSF_CRAG_RESULT_CHOICES,
        default=NOT_APPLICABLE,
        blank=False,
    )

    prior_cm_episode = models.CharField(
        verbose_name="Has the patient had a prior episode of CM or cryptococcal antigenaemia?",
        max_length=25,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
        blank=False,
    )

    reaction_to_study_drugs = models.CharField(
        verbose_name="Has the patient had any serious reaction to flucytosine or fluconazole?",
        max_length=25,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
        blank=False,
    )

    # exclusion
    on_flucon = models.CharField(
        verbose_name=(
            # As per '01_Screening Form_110821_V0.5.pdf' / 'EFFECT Protocol V1.2 7July 2021'
            "Is the patient already taking high-dose fluconazole treatment "
            "(800-1200 mg/day) for ≥1 week?"
        ),
        max_length=25,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
        blank=False,
    )

    # exclusion
    contraindicated_meds = models.CharField(
        verbose_name="Is the patient taking any contraindicated " "concomitant medications?",
        max_length=25,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
        blank=False,
        help_text="Refer to the protocol for a complete list.",
    )

    # exclusion
    mg_severe_headache = models.CharField(
        verbose_name="a progressively severe headache?",
        max_length=25,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
        blank=False,
    )

    # exclusion
    mg_headache_nuchal_rigidity = models.CharField(
        verbose_name="a headache and marked nuchal rigidity?",
        max_length=25,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
        blank=False,
    )

    # exclusion
    mg_headache_vomiting = models.CharField(
        verbose_name="a headache and vomiting?",
        max_length=25,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
        blank=False,
    )

    # exclusion
    mg_seizures = models.CharField(
        verbose_name="seizures?",
        max_length=25,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
        blank=False,
    )

    # exclusion
    mg_gcs_lt_15 = models.CharField(
        verbose_name="a Glasgow Coma Scale (GCS) score of <15?",
        max_length=25,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
        blank=False,
    )

    # exclusion
    any_other_mg_ssx = models.CharField(
        verbose_name="any other clinical symptoms/signs of symptomatic meningitis?",
        max_length=25,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
        blank=False,
    )

    any_other_mg_ssx_other = models.TextField(
        verbose_name="If YES, specify",
        null=True,
        blank=True,
        help_text="If more than one, please separate each with a comma (,).",
    )
    # exclusion
    jaundice = models.CharField(
        verbose_name="Based on clinical examination, does the patient have jaundice?",
        max_length=25,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
        blank=False,
    )

    # TODO: If pending, get at baseline
    cm_in_csf = models.CharField(
        verbose_name="Was CM confirmed in CSF by any other method?",
        max_length=25,
        choices=CSF_YES_NO_PENDING_NA,
        default=NOT_APPLICABLE,
        blank=False,
        help_text=format_html(
            "At any time between the CrAg test and screening for eligibility. "
            "<BR>If results on tests on CSF are `pending`, report on "
            "DAY 1 visit or when available.",
        ),
    )

    cm_in_csf_date = models.DateField(
        verbose_name="Date `pending results` expected (estimate)", null=True, blank=True
    )

    cm_in_csf_method = models.CharField(
        verbose_name="If YES, by which method?",
        max_length=25,
        choices=CM_ON_CSF_METHODS,
        default=NOT_APPLICABLE,
    )

    cm_in_csf_method_other = OtherCharField(max_length=50)

    unsuitable_for_study = models.CharField(
        verbose_name=(
            "Is there any other reason the patient is deemed to not be suitable for the study?"
        ),
        max_length=15,
        choices=YES_NO_NOT_EVALUATED,
        default=NOT_EVALUATED,
        help_text="If YES, patient NOT eligible, please specify reason below ...",
    )

    unsuitable_reason = models.CharField(
        verbose_name="If YES, reason not suitable for the study",
        max_length=30,
        choices=UNSUITABLE_REASONS,
        default=NOT_APPLICABLE,
    )

    unsuitable_reason_other = models.TextField(
        verbose_name="If other reason unsuitable, please specify ...",
        max_length=150,
        null=True,
        blank=True,
    )

    # retired, overrides reasons_unsuitable in ScreeningFieldsModeMixin
    reasons_unsuitable = models.TextField(
        verbose_name="Reason not suitable for the study",
        max_length=150,
        default=QUESTION_RETIRED,
        editable=False,
        help_text="question_retired",
    )

    safe_save_id = models.UUIDField(
        unique=True,
        null=True,
    )

    @property
    def human_readable_identifier(self):
        """Returns a humanized screening identifier."""
        x = self.screening_identifier
        return f"{x[0:4]}-{x[4:]}"

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Subject Screening"
        verbose_name_plural = "Subject Screening"
