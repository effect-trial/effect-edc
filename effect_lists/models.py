from edc_list_data.model_mixins import ListModelMixin


class ArvRegimens(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "ARV Regimens"
        verbose_name_plural = "ARV Regimens"


class OffstudyReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Offstudy Reasons"
        verbose_name_plural = "Offstudy Reasons"


class NeurologicalConditions(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Neurological Conditions"
        verbose_name_plural = "Neurological Conditions"


class NonAdherenceReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Non-Adherence Reasons"
        verbose_name_plural = "Non-Adherence Reasons"


class Symptoms(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Symptoms"
        verbose_name_plural = "Symptoms"


class SubjectVisitMissedReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Subject Missed Visit Reasons"
        verbose_name_plural = "Subject Missed Visit Reasons"
