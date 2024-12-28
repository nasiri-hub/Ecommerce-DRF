from django.contrib import admin
from .models import Tag, TaggedItem


@admin.register(Tag)
class TagAdming(admin.ModelAdmin):
    search_fields = ['label']
    list_display = ['label']


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    model = TaggedItem
    fields = ['tag', 'content_type', 'object_id']
