from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resource import FeedbackResource

from .models import Feedback

class FeedbackAdmin(ImportExportModelAdmin):
    resource_classes = [FeedbackResource]
    
    list_display = ('id','user','title','content','date')
    list_display_links = ('id','user','date')
    search_fields = ('id','user','date')
    list_per_page =25

admin.site.register(Feedback,FeedbackAdmin)