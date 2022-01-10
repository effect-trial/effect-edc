from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models

from ..choices import (
    ACTIVITY_CHOICES,
    CHILDCARE_CHOICES,
    PAYEE_CHOICES,
    TRANSPORT_CHOICES,
)
from ..model_mixins import CrfModelMixin


class HealthEconomics(CrfModelMixin, edc_models.BaseUuidModel):

    """Original but retired HE form.

    Was retired just before 3 months in"""

    occupation = models.CharField(
        verbose_name="What is your occupation/profession?", max_length=50
    )

    education_in_years = models.IntegerField(
        verbose_name="How many years of education did you compete?",
        validators=[MinValueValidator(0), MaxValueValidator(30)],
    )

    education_certificate = models.CharField(
        verbose_name="What is your highest education certificate?", max_length=50
    )

    primary_school = models.CharField(
        verbose_name="Did you go to primary/elementary school?",
        max_length=15,
        choices=YES_NO,
    )

    primary_school_in_years = models.IntegerField(
        verbose_name="If YES, for how many years",
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )

    secondary_school = models.CharField(
        verbose_name="Did you go to secondary school?", max_length=15, choices=YES_NO
    )

    secondary_school_in_years = models.IntegerField(
        verbose_name="If YES, for how many years",
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
    )

    higher_education = models.CharField(
        verbose_name="Did you go to higher education?", max_length=15, choices=YES_NO
    )

    higher_education_in_years = models.IntegerField(
        verbose_name="If YES, for how many years",
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
    )

    welfare = models.CharField(
        verbose_name="Do you receive any welfare or social service support",
        max_length=15,
        choices=YES_NO,
    )

    household_income_per_month = models.IntegerField(
        verbose_name="What is the total income in your household per month?",
        help_text="Rand or  Shilling",
    )

    is_highest_earner = models.CharField(
        verbose_name=(
            "Are you the person who earns the highest income in your household?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    highest_earner = models.CharField(
        verbose_name=(
            "If NO, what is the profession of the person "
            "who earns the highest income?"
        ),
        max_length=50,
        null=True,
        blank=True,
    )

    food_per_month = models.IntegerField(
        verbose_name="How much do your family spend on food in a month?",
        help_text="Rand or  Shilling",
    )

    accommodation_per_month = models.IntegerField(
        verbose_name=(
            "How much does your household spend on rent "
            "(or house loan/mortgage) and utilities in a month?"
        ),
        help_text="Rand or  Shilling",
    )

    large_expenditure_year = models.IntegerField(
        verbose_name="How much have you spent on large items in the last year",
        help_text="e.g. furniture, electrical items, cars (Rand or  Shilling)",
    )

    buy_meds_month = models.CharField(
        verbose_name="Over the last month, did you get any drugs or have a drug refill?",
        max_length=15,
        choices=YES_NO,
    )

    arv_expenditure_month = models.IntegerField(
        verbose_name="If YES, how much did you spend on Antiretroviral drugs",
        help_text="Rand or  Shilling",
        null=True,
        blank=True,
    )

    arv_payee = models.CharField(
        verbose_name="If YES, how did you pay or who paid for other drugs",
        max_length=15,
        choices=PAYEE_CHOICES,
    )

    other_drugs_expenditure_month = models.IntegerField(
        verbose_name="If YES, how much did you spend on 'other' drugs relief",
        help_text="Rand or  Shilling",
        null=True,
        blank=True,
    )

    other_drugs_payee = models.CharField(
        verbose_name="If YES, how did you pay or who paid for these drugs relief",
        max_length=15,
        choices=PAYEE_CHOICES,
    )

    expenditure_other_month = models.CharField(
        verbose_name=(
            "Over the last month, did you spend money on other activities (not drugs) "
            "relating to your health?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    expenditure_other_detail = models.TextField(
        verbose_name="If YES, what was the activity", null=True, blank=True
    )

    expenditure_other = models.IntegerField(
        verbose_name=(
            "If YES, how much was spent on other activities "
            "(not drugs) relating to your health?"
        ),
        help_text="Rand or  Shilling",
        null=True,
        blank=True,
    )

    expenditure_other_payee = models.CharField(
        verbose_name="If YES, how did you pay or who paid for these activities?",
        max_length=15,
        choices=PAYEE_CHOICES,
    )

    normal_activities_disrupted = models.IntegerField(
        verbose_name=(
            "Over the last month, how many days were your normal activities "
            "disrupted through illness?"
        ),
        help_text="in days",
    )

    healthcare_expenditure_month = models.IntegerField(
        verbose_name=(
            "How much in total has been spent on your healthcare in the last month?"
        ),
        help_text="Rand or  Shilling",
    )

    routine_activities = models.CharField(
        verbose_name="What would you be doing if you had not come to the hospital?",
        max_length=25,
        choices=ACTIVITY_CHOICES,
    )

    routine_activities_other = models.CharField(
        verbose_name="If OTHER, please specify", max_length=50, null=True, blank=True
    )

    off_work_days = models.DecimalField(
        verbose_name="How much time did you take off work to come to this appointment?",
        decimal_places=1,
        max_digits=4,
        help_text="in days. (1,2,3 etc. If half-day 0.5)",
    )

    travel_time = models.CharField(
        verbose_name="How long did it take you to reach here?",
        max_length=5,
        help_text="in hours and minutes (format HH:MM)",
    )

    hospital_time = models.CharField(
        verbose_name="How much time did you spend at the hospital?",
        max_length=5,
        help_text="in hours and minutes (format HH:MM)",
    )

    lost_income = models.CharField(
        verbose_name="Did you lose earnings as a result? ",
        max_length=15,
        choices=YES_NO,
    )

    lost_income_amount = models.IntegerField(
        verbose_name="If Yes, how much did you lose?",
        null=True,
        blank=True,
        help_text="In Rands or Shillings",
    )

    childcare = models.CharField(
        verbose_name=(
            "Did you ask anyone else, such as your family member, "
            "friend to look after your child/children in order to come here?"
        ),
        max_length=15,
        choices=YES_NO_NA,
    )

    childcare_source = models.CharField(
        verbose_name=(
            "If Yes, what would they have been doing if they had not stayed to "
            "look after your child or children?"
        ),
        max_length=25,
        choices=CHILDCARE_CHOICES,
        default=NOT_APPLICABLE,
    )

    childcare_source_other = models.CharField(
        verbose_name="If OTHER, please specify", max_length=50, null=True, blank=True
    )

    childcare_source_time_off = models.DecimalField(
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

    transport_old = models.CharField(
        verbose_name=(
            "Which form of transport did you take to get to the hospital today?"
        ),
        help_text="If more than one, then choose all that apply",
        max_length=25,
        choices=TRANSPORT_CHOICES,
    )

    transport_old_other = models.CharField(
        verbose_name="If OTHER, please specify", max_length=50, null=True, blank=True
    )

    transport_cost = models.IntegerField(
        verbose_name="How much did you spend on transport in total?",
        help_text=(
            "Coming to the health care facility and going back home (in Rand or  Shilling)"
        ),
    )

    spend_food_today = models.IntegerField(
        verbose_name="How much did you spend on food while you were here today?",
        help_text="In Rand or Shillings",
    )

    drug_visit_today = models.CharField(
        verbose_name="Did you get any drugs on your visit today?",
        max_length=15,
        choices=YES_NO,
    )

    spend_on_arv = models.IntegerField(
        verbose_name="If YES, how much did you spend on Antiretroviral drugs",
        help_text="In Rands or Shillings",
    )
    spend_on_arv_payee = models.CharField(
        verbose_name="If YES, how did you pay or who paid for Antiretroviral drugss",
        max_length=15,
        choices=PAYEE_CHOICES,
    )

    spend_on_other = models.IntegerField(
        verbose_name="If YES, how much did you spend on other drugs",
        help_text="In Rands or Shillings",
    )

    spend_on_other_payee = models.CharField(
        verbose_name="If YES, how did you pay or who paid for other drugs",
        max_length=15,
        choices=PAYEE_CHOICES,
    )

    other_activity_health = models.IntegerField(
        verbose_name=(
            "Did you spend money on other activities (not drugs) relating to "
            "your health today?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    which_other_activity_health = models.CharField(
        verbose_name="If YES, what was the activity?"
    )

    amount_other_activity_health = models.IntegerField(
        verbose_name="If YES, how much did you spend?"
    )

    pay_admin_fee_hospital = models.CharField(
        verbose_name=(
            "Did you pay for any administrative fees/charges at the hospital "
            "when you got admitted?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    amount_pay_admin_fee_hospital = models.IntegerField(
        verbose_name="If YES, how much did you pay in hospital charges?",
        help_text="In Rands or Shillings",
    )

    pay_money_test = models.CharField(
        verbose_name=(
            "Did you pay any money to have any tests/investigations done while admitted?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    amount_pay_test = models.IntegerField(
        verbose_name="If YES, how much did you pay", help_text="In Rands or Shillings"
    )

    admitted_day_food_spend = models.IntegerField(
        verbose_name="On the day you were admitted, how much money did you spend on food?",
        help_text="In Rands or Shillings",
    )

    admitted_spend_other = models.IntegerField(
        verbose_name="While you were admitted, how much money did you spend on other items?",
        help_text=(
            "such as airtime, toiletries, soap/shampoo, toothbrush/toothpaste, "
            "bucket/basin for washing, toilet paper, clothes and cups/plates "
            "(In Rands or Shillings)"
        ),
    )

    time_off = models.CharField(
        verbose_name="Did you have to take time off work because of being admitted?",
        max_length=15,
        choices=YES_NO,
    )

    family_friends_stayed = models.IntegerField(
        verbose_name=(
            "How many family members or friends stayed with you in hospital to "
            "look after you during your hospital stay?"
        )
    )

    family_friends_visited = models.IntegerField(
        verbose_name="How many family members or friends visited you during "
        "your hospital stay?"
    )

    family_friends_time_off = models.CharField(
        verbose_name=(
            "Did the family members/friends have to take time off work to stay "
            "with you or to come see you during your hospital stay?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    family_friends_earn = models.IntegerField(
        verbose_name="If they work, how much do they normally earn per month?",
        help_text="In Rand or Shillings",
    )

    sell_anything = models.CharField(
        verbose_name="Did you sell anything to pay for your visit today?",
        max_length=15,
        choices=YES_NO,
    )

    loan_for_visit = models.CharField(
        verbose_name="Did you take any loans to pay for your visit?",
        max_length=15,
        choices=YES_NO,
    )

    private_healthcare_insurance = models.CharField(
        verbose_name="Do you have private healthcare insurance?",
        max_length=15,
        choices=YES_NO,
    )

    amount_private_healthcare_insurance = models.IntegerField(
        verbose_name=(
            "If YES, how much do you pay towards your contributions to "
            "healthcare insurance every month?"
        ),
        help_text="In Rands or Shillings",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Health Economics"
        verbose_name_plural = "Health Economics"
