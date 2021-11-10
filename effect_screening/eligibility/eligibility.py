from edc_constants.constants import NO, TBD, YES
from edc_utils import get_utcnow


class SubjectScreeningEligibilityError(Exception):
    pass


class Eligibility:
    """
    Determines if a subject is eligible or not.

    Eligibility is assessed in three parts.

    Instantiated in the save() method of the screening proxy models.

    For example, for part one:

        def save(self, *args, **kwargs):
            eligibility = Eligibility(self)
            try:
                eligibility.assess_eligibility_for_part_one()
            except EligibilityPartOneError:
                pass
            eligibility.update_eligibility_fields()
            super().save(*args, **kwargs)

    """

    eligibility_values = [YES, NO, TBD]

    def __init__(self, obj):
        self.obj = obj

    def update_eligibility_fields(self):
        """Updates model instance fields `eligible`, `eligibility_datetime` and
        `reasons_ineligible`.
        """
        reasons_ineligible = []
        if self.obj.unsuitable_for_study == YES:
            self.obj.eligible = False
            reasons_ineligible.append("Subject unsuitable")
        else:
            self.obj.eligible = self.is_eligible
        if self.obj.eligible:
            self.obj.reasons_ineligible = None
        else:
            reasons_ineligible = self.get_reasons_if_ineligible(reasons_ineligible)
            if reasons_ineligible:
                self.obj.reasons_ineligible = "|".join(reasons_ineligible)
            else:
                self.obj.reasons_ineligible = None
        self.obj.eligibility_datetime = self.obj.report_datetime or get_utcnow()

    def get_reasons_if_ineligible(self, reasons_ineligible):
        if self.obj.reasons_ineligible:
            reasons_ineligible.append(self.obj.reasons_ineligible)
        return reasons_ineligible

    @property
    def is_eligible(self):
        """Returns True if eligible else False"""
        return True if self.eligible == YES else False

    @property
    def eligible(self):
        """Returns YES, NO or TBD."""
        return self.obj.eligible

    @property
    def eligibility_display_label(self):
        return ""

    @property
    def eligibility_status(self):
        status_str = self.obj.eligible.upper()
        display_label = self.eligibility_display_label

        if "PENDING" in display_label:
            display_label = f'<font color="orange"><B>{display_label}</B></font>'

        return status_str + display_label
