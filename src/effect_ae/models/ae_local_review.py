from edc_model.models import BaseUuidModel

from ..model_mixins import AeReviewModelMixin


class AeLocalReview(AeReviewModelMixin, BaseUuidModel):
    """Not used"""

    class Meta(BaseUuidModel.Meta):
        verbose_name = "AE Local Review"
