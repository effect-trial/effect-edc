from edc_list_data.model_mixins import ListModelMixin


class Antibiotics(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Antibiotics"
        verbose_name_plural = "Antibiotics"


class ArvRegimens(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "ARV Regimens"
        verbose_name_plural = "ARV Regimens"


class Drugs(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Drugs"
        verbose_name_plural = "Drugs"


class FocalNeurologicDeficits(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Focal Neurologic Deficits"
        verbose_name_plural = "Focal Neurologic Deficits"


class OffstudyReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Offstudy Reasons"
        verbose_name_plural = "Offstudy Reasons"


class MedicinesRxDay14(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Medicines Prescribed Day 14"
        verbose_name_plural = "Medicines Prescribed Day 14"


class NonAdherenceReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Non-Adherence Reasons"
        verbose_name_plural = "Non-Adherence Reasons"


class SignificantNewDiagnoses(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Significant New Diagnoses"
        verbose_name_plural = "Significant New Diagnoses"


class Symptoms(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Symptoms"
        verbose_name_plural = "Symptoms"


class SubjectVisitMissedReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Subject Missed Visit Reasons"
        verbose_name_plural = "Subject Missed Visit Reasons"


class TbTreatments(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "TB Treatments"
        verbose_name_plural = "TB Treatments"


class XRayResults(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "X-Ray Results"
        verbose_name_plural = "X-Ray Results"
