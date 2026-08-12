from django.contrib import admin

from .models import Stuff

class StuffAdmin(admin.ModelAdmin):
    list_display = ('id','user','name','type','description','location','missing_date','photo_main','district')
    list_display_links = ('id','name')
    search_fields = ('type','user','status')
    list_per_page =25

admin.site.register(Stuff,StuffAdmin)