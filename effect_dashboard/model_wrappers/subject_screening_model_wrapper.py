from edc_consent import site_consents
from edc_consent.consent_definition import ConsentDefinition
from edc_screening.model_wrappers import (
    SubjectScreeningModelWrapper as BaseSubjectScreeningModelWrapper,
)
from edc_screening.utils import get_subject_screening_model
from edc_sites import site_sites
from edc_subject_model_wrappers import (
    SubjectConsentModelWrapper as BaseSubjectConsentModelWrapper,
)


class SubjectConsentModelWrapper(BaseSubjectConsentModelWrapper):
    @property
    def querystring(self):
        return (
            f"cancel=effect_dashboard:screening_listboard_url,"
            f"screening_identifier&{super().querystring}"
        )


class SubjectScreeningModelWrapper(BaseSubjectScreeningModelWrapper):
    model = get_subject_screening_model()

    consent_model_wrapper_cls = SubjectConsentModelWrapper

    @property
    def consent_definition(self) -> ConsentDefinition:
        """Returns a consent definition relative to the wrapper's
        `self.object` report_datetime and site.

        In this case, `self.object` is an instance of the
        subjectscreening model.
        """
        if not self._consent_definition:
            self._consent_definition = site_consents.get_consent_definition(
                # model=self.model_name,
                report_datetime=self.report_datetime,
                site=site_sites.get(self.object.site.id),
            )
        return self._consent_definition
