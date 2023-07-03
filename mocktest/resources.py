from import_export import resources
from .models import Test

class TestResource(resources.ModelResource):
    class Meta:
        model = Test
        fields = ('id', 'course', 'topic', 'title', 'description')
