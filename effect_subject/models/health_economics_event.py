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
    PAYEE_CHOICES_ACTIVITIES,
    PAYEE_CHOICES_DRUGS,
)
from ..model_mixins import CrfModelMixin


class HealthEconomicsEvent(CrfModelMixin, edc_models.BaseUuidModel):
    buy_refill_drug = models.CharField(
        verbose_name=(
            "Over the past period since your treatment, did you buy any drugs or "
            "have a drug refill?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    amount_spent_antiretroviral_drugs_past = models.IntegerField(
        verbose_name="If YES, how much did you spend on antiretroviral drugs?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    amount_spent_other_drugs_past = models.IntegerField(
        verbose_name="If YES, how much did you spend on other drugs for relief?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    payment_method_antiretroviral_drugs_past = models.CharField(
        verbose_name="If spent on antiretroviral drugs, how did you pay or who paid for them?",
        max_length=45,
        choices=PAYEE_CHOICES_DRUGS,
        default=NOT_APPLICABLE,
    )

    payment_method_other_drugs_past = models.CharField(
        verbose_name=(
            "If spent on other drugs for relief, how did you pay or who paid for them?"
        ),
        max_length=45,
        choices=PAYEE_CHOICES_DRUGS,
        default=NOT_APPLICABLE,
    )

    spent_money_other_health_activities_past = models.CharField(
        verbose_name=(
            "Since your last study visit, did you spend money on other activities "
            "(not drugs) relating to your health?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    other_health_activities_past = models.CharField(
        verbose_name="If YES, what was the activity?",
        max_length=145,
        blank=True,
        null=True,
    )

    amount_spent_other_health_activities_past = models.IntegerField(
        verbose_name=(
            "If YES, how much was spent on other activities (not drugs) relating to "
            "your health?"
        ),
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text="In rands or shillings",
    )

    payment_method_other_health_activities_past = models.CharField(
        verbose_name="If YES, how did you pay or who paid for these activities?",
        max_length=45,
        choices=PAYEE_CHOICES_ACTIVITIES,
    )

    num_day_activities_disrupted = models.IntegerField(
        verbose_name=(
            "Over the past period since your treatment, how many days were your "
            "normal activities disrupted through illness?"
        ),
        validators=[MinValueValidator(0)],
    )

    amount_spent_healthcare_last_month = models.IntegerField(
        verbose_name="How much in total has been spent on your healthcare in the last month?",
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
    )

    activities_not_come_clinic = models.CharField(
        verbose_name=(
            "What would you be doing in your life, if you had not come to the "
            "hospital or clinic?"
        ),
        max_length=45,
        choices=ACTIVITY_CHOICES,
    )

    activities_not_come_clinic_other = edc_models.OtherCharField()

    time_taken_off_work = models.DecimalField(
        verbose_name="How much time did you take off work to come to this appointment?",
        decimal_places=1,
        max_digits=4,
        help_text="in days. (1,2,3 etc. If half-day 0.5)",
    )

    time_taken_get_here = models.CharField(
        verbose_name="How long did it take you to reach here?",
        validators=[hm_validator],
        max_length=5,
        help_text="in hours and minutes (format HH:MM)",
    )

    time_spent_clinic = models.CharField(
        verbose_name="How much time did you spend at the hospital or clinic?",
        validators=[hm_validator],
        max_length=5,
        help_text="in hours and minutes (format HH:MM)",
    )

    loss_earnings = models.CharField(
        verbose_name="Did you lose earnings as a result?",
        max_length=15,
        choices=YES_NO,
    )

    loss_earnings_amount = models.IntegerField(
        verbose_name="If YES, how much did you lose?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    someone_looking_children = models.CharField(
        verbose_name=(
            "Did you ask anyone else, such as your family member, friend to look "
            "after your child/children in order to come here?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    someone_looking_children_activities = models.CharField(
        verbose_name=(
            "If YES, what would they have been doing if they had not stayed to look "
            "after your child or children?"
        ),
        max_length=45,
        choices=ACTIVITY_CHOICES_NA,
        default=NOT_APPLICABLE,
    )

    someone_looking_children_activities_other = edc_models.OtherCharField()

    someone_looking_children_time_spent = models.DecimalField(
        verbose_name=(
            "How much time did a family member, friend take off work to look "
            "after your child or children?"
        ),
        decimal_places=1,
        max_digits=4,
        null=True,
        blank=True,
        help_text="in days. (1,2,3 etc. If half-day 0.5)",
    )

    transport_used = models.ManyToManyField(
        Transport,
        verbose_name=(
            "Which form of transport did you use to come to the hospital/clinic today?"
        ),
        help_text="If more than one, select all that apply.",
    )

    transport_used_other = edc_models.OtherCharField()

    transport_used_amount = models.IntegerField(
        verbose_name=(
            "How much will you spend on transport in total (coming to the health "
            "care facility and going back home)?"
        ),
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
    )

    amount_spent_food = models.IntegerField(
        verbose_name="How much did you spend on food while you were here today?",
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
    )

    get_drugs_visit_today = models.CharField(
        verbose_name="Did you get any drugs on your visit today?",
        max_length=15,
        choices=YES_NO,
    )

    amount_spent_antiretroviral_drugs_today = models.IntegerField(
        verbose_name="If YES, how much did you spend on antiretroviral drugs?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    amount_spent_other_drugs_today = models.IntegerField(
        verbose_name="If YES, how much did you spend on other drugs for relief?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    payment_method_antiretroviral_drugs_today = models.CharField(
        verbose_name="If spent on antiretroviral drugs, how did you pay or who paid for them?",
        max_length=45,
        choices=PAYEE_CHOICES_DRUGS,
        default=NOT_APPLICABLE,
    )

    payment_method_other_drugs_today = models.CharField(
        verbose_name=(
            "If spent on other drugs for relief, how did you pay or who paid for them?"
        ),
        max_length=45,
        choices=PAYEE_CHOICES_DRUGS,
        default=NOT_APPLICABLE,
    )

    spent_money_other_health_activities_today = models.CharField(
        verbose_name=(
            "Did you spend money on other activities (not drugs) relating to your "
            "health today?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    other_health_activities_today = models.CharField(
        verbose_name="If YES, what was the activity?",
        max_length=145,
        null=True,
        blank=True,
    )

    amount_spent_other_health_activities_today = models.IntegerField(
        verbose_name="If YES, how much did you spend?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    administrative_charges = models.CharField(
        verbose_name=(
            "Did you pay for any administrative fees/charges at the hospital when "
            "you got admitted?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    administrative_charges_amount = models.IntegerField(
        verbose_name="If YES, how much did you pay in hospital charges?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    admitted_day_pay_for_tests = models.CharField(
        verbose_name=(
            "Did you pay any money to have any tests/investigations done while admitted?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    admitted_day_amount_pay_for_tests = models.IntegerField(
        verbose_name="If YES, how much did you pay?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    admitted_day_amount_spent_food = models.IntegerField(
        verbose_name="On the day you were admitted, how much money did you spend on food?",
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
    )

    admitted_amount_spent_other_items = models.IntegerField(
        verbose_name=(
            "While you were admitted, how much money did you spend on other items "
            "such as airtime,toiletries (soap/shampoo, toothbrush/toothpaste, bucket/basin "
            "for washing, toilet paper), clothes and cups/plates?"
        ),
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
    )

    admitted_time_off_work = models.CharField(
        verbose_name="Did you have to take time off work because of being admitted?",
        max_length=15,
        choices=YES_NO,
    )

    admitted_num_people_stay_with_you = models.IntegerField(
        verbose_name=(
            "How many family members or friends stayed with you in hospital to look "
            "after you during your hospital stay?"
        ),
    )

    admitted_num_people_visit_you = models.IntegerField(
        verbose_name=(
            "How many family members or friends visited you during your hospital stay?"
        ),
    )

    admitted_people_time_off_work = models.CharField(
        verbose_name=(
            "Did a family member/friend have to take time off work to stay with you "
            "or to come see you during your hospital stay?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    admitted_people_time_off_work_amount_monthly = models.IntegerField(
        verbose_name=(
            "If YES, and they work, how much does this person normally earn per month?"
        ),
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In rands or shillings",
    )

    sale_anything_pay_visit_today = models.CharField(
        verbose_name="Did you sell anything to pay for your visit today?",
        max_length=15,
        choices=YES_NO,
    )

    loan_pay_visit_treatment = models.CharField(
        verbose_name="Did you take any loans to pay for your visit or treatment?",
        max_length=15,
        choices=YES_NO,
    )

    private_healthcare = models.CharField(
        verbose_name="Do you have private healthcare insurance?",
        max_length=15,
        choices=YES_NO,
    )

    private_healthcare_amount_monthly = models.IntegerField(
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
