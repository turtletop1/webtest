from django.contrib import admin

from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','user','post','content','date')
    list_display_links = ('id','user','post')
    search_fields = ('id','user','post')
    list_per_page =25

admin.site.register(Comment,CommentAdmin)