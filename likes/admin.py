from django.contrib import admin
from .models import LikedItem


@admin.register(LikedItem)
class LikedItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'object_id', 'content_object']
    autocomplete_fields = ['user']
