from import_export import resources
from .models import Feedback


class FeedbackResource(resources.ModelResource):
    class Meta:
        model = Feedback