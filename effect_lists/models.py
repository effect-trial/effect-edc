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


class MedicinesDay14(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Medicines Prescribed Day 14"
        verbose_name_plural = "Medicines Prescribed Day 14"


class NonAdherenceReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Non-Adherence Reasons"
        verbose_name_plural = "Non-Adherence Reasons"


class Dx(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Diagnoses"
        verbose_name_plural = "Diagnoses"


class SiSx(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Signs and Symptoms"
        verbose_name_plural = "Signs and Symptoms"


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
