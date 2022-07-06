from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models

from effect_lists.models import Transport

from ..choices import (
    CHILDCARE_CHOICES,
    CHILDCARE_ECON_CHOICES,
    PAYEE_CHOICES,
    PAYEE_CHOICES_ECON,
)
from ..model_mixins import CrfModelMixin


class HealthEconomicsEvent(CrfModelMixin, edc_models.BaseUuidModel):
    buy_refill_drug = models.CharField(
        verbose_name="Over the past period since your treatment, did you buy any drugs or "
        "had drug refill?",
        max_length=15,
        choices=YES_NO,
    )

    amount_spent_antiretroviral_drugs_past = models.IntegerField(
        verbose_name="How much did you spend on Antiretroviral drugs",
    )

    amount_spent_other_drugs_past = models.IntegerField(
        verbose_name="How much did you spend on Other drugs for relief",
    )

    payment_method_antiretroviral_drugs_past = models.CharField(
        verbose_name="If YES, how did you pay or who paid for Antiretroviral drugs?",
        max_length=45,
        choices=PAYEE_CHOICES,
        default=NOT_APPLICABLE,
    )

    payment_method_other_drugs_past = models.CharField(
        verbose_name="If YES, how did you pay or who paid for Antiretroviral drugs?If YES, "
        "how did you pay or who paid for Other drugs for relief?",
        max_length=45,
        choices=PAYEE_CHOICES,
        default=NOT_APPLICABLE,
    )

    spent_money_other_health_activities_past = models.CharField(
        verbose_name="Since your last study visit, did you spend money on other activities ("
        "not drugs) relating to your health?",
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
        verbose_name="If YES, how much was spent on other activities (not drugs) relating to "
        "your health?",
    )

    payment_method_other_health_activities_past = models.CharField(
        verbose_name="If YES, how did you pay or who paid for these activities?",
        max_length=45,
        choices=PAYEE_CHOICES_ECON,
    )

    num_day_activities_disrupted = models.IntegerField(
        verbose_name="Over the past period since your treatment, how many days were your "
        "normal activities disrupted through illness?",
    )

    amount_spent_healthcare_last_month = models.IntegerField(
        verbose_name="How much in total has been spent on your healthcare in the last month?"
    )

    activities_not_come_clinic = models.CharField(
        verbose_name="What would you be doing in your life, if you had not come to the "
        "hospital or clinic",
        max_length=45,
        choices=CHILDCARE_ECON_CHOICES,
    )

    activities_not_come_clinic_other = edc_models.OtherCharField()

    time_taken_off_work = models.IntegerField(
        verbose_name="How much time did you take off work to come to this appointment?",
    )

    time_taken_get_here = models.TimeField(
        verbose_name="How long did it take you to reach here?",
    )

    time_spent_clinic = models.IntegerField(
        verbose_name="How much time did you spend at the hospital or clinic?",
    )

    loss_earnings = models.CharField(
        verbose_name="Did you lose earnings as a result?",
        max_length=15,
        choices=YES_NO,
    )

    loss_earnings_amount = models.IntegerField(
        verbose_name="If YES, how much did you lose?",
    )

    someone_looking_children = models.CharField(
        verbose_name="Did you ask anyone else, such as your family member, friend to look "
        "after your child/children from .health_economics_event_form import "
        "HealthEconomicsEventFormin order to come here?",
        max_length=15,
        choices=YES_NO_NA,
    )
    someone_looking_children_activities = models.CharField(
        verbose_name="If YES, what would they have been doing if they had not stayed to look "
        "after your child or children?",
        max_length=45,
        choices=CHILDCARE_CHOICES,
    )
    someone_looking_children_activities_other = edc_models.OtherCharField()

    someone_looking_children_time_spent = models.IntegerField(
        verbose_name="How much time did a family member, friend take off work to look after "
        "your child or children?",
    )

    transport_used = models.ManyToManyField(
        Transport,
        verbose_name="Which form of transport did you use to come to the hospital/clinic "
        "today?",
    )

    transport_used_other = edc_models.OtherCharField()

    transport_used_amount = models.IntegerField(
        verbose_name="How much will you spend on transport in total (coming to the health "
        "care facility and going back home)?",
    )

    amount_spent_food = models.IntegerField(
        verbose_name="How much did you spend on food while you were here today?"
    )
    get_drugs_visit_today = models.CharField(
        verbose_name="Did you get any drugs on your visit today?",
        max_length=15,
        choices=YES_NO,
    )

    amount_spent_antiretroviral_drugs_today = models.IntegerField(
        verbose_name="How much did you spend on Antiretroviral drugs",
    )

    amount_spent_other_drugs_today = models.IntegerField(
        verbose_name="How much did you spend on other drugs"
    )

    payment_method_antiretroviral_drugs_today = models.CharField(
        verbose_name="how did you pay or who paid for Antiretroviral drugs",
        max_length=45,
        choices=PAYEE_CHOICES,
        default=NOT_APPLICABLE,
    )

    payment_method_other_drugs_today = models.CharField(
        verbose_name="how did you pay or who paid for other drugs",
        max_length=45,
        choices=PAYEE_CHOICES,
        default=NOT_APPLICABLE,
    )

    spent_money_other_health_activities_today = models.CharField(
        verbose_name="Did you spend money on other activities (not drugs) relating to your "
        "health today?",
        max_length=15,
        choices=YES_NO,
    )

    other_health_activities_today = models.CharField(
        verbose_name="If YES, what was the activity?",
        max_length=145,
        blank=True,
        null=True,
    )

    amount_spent_other_health_activities_today = models.IntegerField(
        verbose_name="If YES, how much did you spend?",
    )

    administrative_charges = models.CharField(
        verbose_name="Did you pay for any administrative fees/charges at the hospital when "
        "you got admitted?",
        max_length=15,
        choices=YES_NO,
    )

    administrative_charges_amount = models.IntegerField(
        verbose_name="If YES, how much did you pay in hospital charges?"
    )

    admitted_day_pay_for_tests = models.CharField(
        verbose_name="Did you pay any money to have any tests/investigations done while "
        "admitted?",
        max_length=15,
        choices=YES_NO,
    )

    admitted_day_amount_pay_for_tests = models.IntegerField(
        verbose_name="f YES, how much did you pay?",
    )

    admitted_day_amount_spent_food = models.IntegerField(
        verbose_name="On the day you were admitted, how much money did you spend on food?",
    )

    admitted_amount_spent_other_items = models.IntegerField(
        verbose_name="While you were admitted, how much money did you spend on other items "
        "such as airtime,toiletries (soap/shampoo, toothbrush/toothpaste, bucket/basin for "
        "washing, toilet paper),clothes and cups/plates?",
    )

    admitted_time_off_work = models.CharField(
        verbose_name="Did you have to take time off work because of being admitted?",
        max_length=15,
        choices=YES_NO,
    )

    admitted_num_people_stay_with_you = models.IntegerField(
        verbose_name="How many family members or friends stayed with you in hospital to look "
        "after you during your hospital stay?",
    )

    admitted_num_people_visit_you = models.IntegerField(
        verbose_name="How many family members or friends visited you during your hospital "
        "stay?",
    )

    admitted_people_time_off_work = models.CharField(
        verbose_name="Did a family member/friend have to take time off work to stay with you "
        "or to come see you during your hospital stay?",
        max_length=15,
        choices=YES_NO,
    )

    admitted_people_time_off_work_amount_monthly = models.IntegerField(
        verbose_name="If they work, how much does this person normally earn per month?",
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
        verbose_name="If YES, how much do you pay towards your contributions to healthcare "
        "insurance every month? "
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Health Economics: Health Event"
        verbose_name_plural = "Health Economics: Health Event"
