from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resource import CommentResource

from .models import Comment

class CommentAdmin(ImportExportModelAdmin):
    resource_classes = [CommentResource]

    list_display = ('id','user','post','content','date')
    list_display_links = ('id','user','post')
    search_fields = ('id','user','post')
    list_per_page =25

admin.site.register(Comment,CommentAdmin)