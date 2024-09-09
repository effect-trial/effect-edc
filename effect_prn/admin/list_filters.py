from edc_model_admin.list_filters import PastDateListFilter


class AdmittedDateListFilter(PastDateListFilter):
    title = "Date admitted"

    parameter_name = "admitted_date"
    field_name = "admitted_date"


class DischargedDateListFilter(PastDateListFilter):
    title = "Date discharged"

    parameter_name = "discharged_date"
    field_name = "discharged_date"
