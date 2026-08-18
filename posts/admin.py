from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resource import PostResource

from .models import Post


class PostAdmin(ImportExportModelAdmin):        #class PostAdmin(admin.ModelAdmin)
    resource_classes = [PostResource]
    
    list_display = ('id', 'title', 'content', 'issue_date', 'user', 'stuff', 'status', 'type', 'due_date', 'reward')
    list_display_links = ('id', 'title', 'content')
    search_fields = ('issue_date', 'user', 'status', 'stuff', 'type')
    list_per_page = 25

admin.site.register(Post, PostAdmin)