from django.contrib import admin
from .models import User_message


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "content", "date")
    list_display_links = ("id", "sender","receiver")
    list_filter = ("date", "sender", "receiver")
    search_fields = ("sender__username","receiver__username","content",)
    list_per_page =25

admin.site.register(User_message,UserMessageAdmin)