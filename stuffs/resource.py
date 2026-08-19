from import_export import resources
from .models import Stuff


class StuffResource(resources.ModelResource):
    class Meta:
        model = Stuff