from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models
from edc_model.validators import hm_validator

from effect_lists.models import Transport

from ..choices import (
    ACTIVITY_CHOICES,
    ACTIVITY_CHOICES_NA,
    LOST_INCOME_CHOICES,
    PAYEE_CHOICES_ACTIVITIES,
    PAYEE_CHOICES_DRUGS,
    TIME_OFF_WORK_CHOICES,
)
from ..model_mixins import CrfModelMixin


class HealthEconomicsEvent(CrfModelMixin, edc_models.BaseUuidModel):

    buy_meds = models.CharField(
        verbose_name=(
            "Over the past period since your treatment, did you buy any drugs or "
            "have a drug refill?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    arv_spend = models.IntegerField(
        verbose_name="If YES, how much did you spend on antiretroviral drugs?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    meds_other_spend = models.IntegerField(
        verbose_name="If YES, how much did you spend on other drugs for relief?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    arv_payee = models.CharField(
        verbose_name="If spent on antiretroviral drugs, how did you pay or who paid for them?",
        max_length=45,
        choices=PAYEE_CHOICES_DRUGS,
        default=NOT_APPLICABLE,
    )

    meds_other_payee = models.CharField(
        verbose_name=(
            "If spent on other drugs for relief, how did you pay or who paid for them?"
        ),
        max_length=45,
        choices=PAYEE_CHOICES_DRUGS,
        default=NOT_APPLICABLE,
    )

    health_activities = models.CharField(
        verbose_name=(
            "Since your last study visit, did you spend money on other activities "
            "(not drugs) relating to your health?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    health_activities_detail = models.CharField(
        verbose_name="If YES, what was the activity?",
        max_length=145,
        blank=True,
        null=True,
    )

    health_activities_spend = models.IntegerField(
        verbose_name=(
            "If YES, how much was spent on other activities (not drugs) relating to "
            "your health?"
        ),
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text="In rands or shillings",
    )

    health_activities_payee = models.CharField(
        verbose_name="If YES, how did you pay or who paid for these activities?",
        max_length=45,
        choices=PAYEE_CHOICES_ACTIVITIES,
        default=NOT_APPLICABLE,
    )

    routine_activities_disrupted_days = models.IntegerField(
        verbose_name=(
            "Over the past period since your treatment, how many days were your "
            "normal activities disrupted through illness?"
        ),
        validators=[MinValueValidator(0)],
    )

    healthcare_month = models.IntegerField(
        verbose_name="How much in total has been spent on your healthcare in the last month?",
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
    )

    routine_activities = models.CharField(
        verbose_name=(
            "What would you be doing in your life, if you had not come to the "
            "hospital or clinic?"
        ),
        max_length=45,
        choices=ACTIVITY_CHOICES,
    )

    routine_activities_other = edc_models.OtherCharField()

    time_off_days = models.DecimalField(
        verbose_name="How much time did you take off work to come to this appointment?",
        decimal_places=1,
        max_digits=4,
        help_text="in days. (1,2,3 etc. If half-day 0.5)",
    )

    travel_time = models.CharField(
        verbose_name="How long did it take you to reach here?",
        validators=[hm_validator],
        max_length=5,
        help_text="in hours and minutes (format HH:MM)",
    )

    hospital_time = models.CharField(
        verbose_name="How much time did you spend at the hospital or clinic?",
        validators=[hm_validator],
        max_length=5,
        help_text="in hours and minutes (format HH:MM)",
    )

    lost_income = models.CharField(
        verbose_name="Did you lose earnings as a result?",
        max_length=15,
        choices=LOST_INCOME_CHOICES,
        default=NOT_APPLICABLE,
    )

    lost_income_amount = models.IntegerField(
        verbose_name="If YES, how much did you lose?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    childcare = models.CharField(
        verbose_name=(
            "Did you ask anyone else, such as your family member, friend to look "
            "after your child/children in order to come here?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    childcare_source = models.CharField(
        verbose_name=(
            "If YES, what would they have been doing if they had not stayed to look "
            "after your child or children?"
        ),
        max_length=45,
        choices=ACTIVITY_CHOICES_NA,
        default=NOT_APPLICABLE,
    )

    childcare_source_other = edc_models.OtherCharField()

    childcare_source_time_off_days = models.DecimalField(
        verbose_name=(
            "If YES, how much time did a family member, friend take off work to look "
            "after your child or children?"
        ),
        decimal_places=1,
        max_digits=4,
        null=True,
        blank=True,
        help_text="in days. (1,2,3 etc. If half-day 0.5)",
    )

    transport = models.ManyToManyField(
        Transport,
        verbose_name=(
            "Which form of transport did you use to come to the hospital/clinic today?"
        ),
        help_text="If more than one, select all that apply.",
    )

    transport_other = edc_models.OtherCharField()

    transport_spend = models.IntegerField(
        verbose_name=(
            "How much will you spend on transport in total (coming to the health "
            "care facility and going back home)?"
        ),
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
    )

    food_spend = models.IntegerField(
        verbose_name="How much did you spend on food while you were here today?",
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
    )

    buy_meds_today = models.CharField(
        verbose_name="Did you get any drugs on your visit today?",
        max_length=15,
        choices=YES_NO,
    )

    arv_spend_today = models.IntegerField(
        verbose_name="If YES, how much did you spend on antiretroviral drugs?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    meds_other_spend_today = models.IntegerField(
        verbose_name="If YES, how much did you spend on other drugs for relief?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    arv_payee_today = models.CharField(
        verbose_name="If spent on antiretroviral drugs, how did you pay or who paid for them?",
        max_length=45,
        choices=PAYEE_CHOICES_DRUGS,
        default=NOT_APPLICABLE,
    )

    meds_other_payee_today = models.CharField(
        verbose_name=(
            "If spent on other drugs for relief, how did you pay or who paid for them?"
        ),
        max_length=45,
        choices=PAYEE_CHOICES_DRUGS,
        default=NOT_APPLICABLE,
    )

    health_activities_today = models.CharField(
        verbose_name=(
            "Did you spend money on other activities (not drugs) relating to your "
            "health today?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    health_activities_detail_today = models.CharField(
        verbose_name="If YES, what was the activity?",
        max_length=145,
        null=True,
        blank=True,
    )

    health_activities_spend_today = models.IntegerField(
        verbose_name="If YES, how much did you spend?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    admitted = models.CharField(
        verbose_name="Was the participant admitted as part of this health event?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    admitted_admin = models.CharField(
        verbose_name=(
            "Did you pay for any administrative fees/charges at the hospital when "
            "you got admitted?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    admitted_admin_spend = models.IntegerField(
        verbose_name="If YES, how much did you pay in hospital charges?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    admitted_investigations = models.CharField(
        verbose_name=(
            "Did you pay any money to have any tests/investigations done while admitted?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    admitted_investigations_spend = models.IntegerField(
        verbose_name="If YES, how much did you pay?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    admitted_food_spend = models.IntegerField(
        verbose_name="On the day you were admitted, how much money did you spend on food?",
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
    )

    admitted_other_spend = models.IntegerField(
        verbose_name=(
            "While you were admitted, how much money did you spend on other items "
            "such as airtime, toiletries (soap/shampoo, toothbrush/toothpaste, bucket/basin "
            "for washing, toilet paper), clothes and cups/plates?"
        ),
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
    )

    admitted_time_off = models.CharField(
        verbose_name="Did you have to take time off work because of being admitted?",
        max_length=15,
        choices=TIME_OFF_WORK_CHOICES,
        default=NOT_APPLICABLE,
    )

    admitted_carers = models.IntegerField(
        verbose_name=(
            "How many family members or friends stayed with you in hospital to look "
            "after you during your hospital stay?"
        ),
    )

    admitted_visitors = models.IntegerField(
        verbose_name=(
            "How many family members or friends visited you during your hospital stay?"
        ),
        validators=[MinValueValidator(0)],
    )

    admitted_kith_kin_time_off = models.CharField(
        verbose_name=(
            "Did a family member/friend have to take time off work to stay with you "
            "or to come see you during your hospital stay?"
        ),
        max_length=15,
        choices=TIME_OFF_WORK_CHOICES,
        default=NOT_APPLICABLE,
    )

    admitted_kith_kin_month = models.IntegerField(
        verbose_name="If YES, how much does this person normally earn per month?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    sell_to_pay = models.CharField(
        verbose_name="Did you sell anything to pay for your visit today?",
        max_length=15,
        choices=YES_NO,
    )

    borrow_to_pay = models.CharField(
        verbose_name="Did you take any loans to pay for your visit or treatment?",
        max_length=15,
        choices=YES_NO,
    )

    health_insurance = models.CharField(
        verbose_name="Do you have private healthcare insurance?",
        max_length=15,
        choices=YES_NO,
    )

    health_insurance_month = models.IntegerField(
        verbose_name=(
            "If YES, how much do you pay towards your contributions to healthcare "
            "insurance every month?"
        ),
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
        null=True,
        blank=True,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Health Economics: Health Event"
        verbose_name_plural = "Health Economics: Health Event"
