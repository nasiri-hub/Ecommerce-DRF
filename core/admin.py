from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem
from likes.models import LikedItem
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'usable_password', 'password1', 'password2', 'email', 'first_name', 'last_name'),
            },
        ),
    )
    search_fields = ['first_name']


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    extra = 0
    model = TaggedItem


class LikedItemInline(GenericTabularInline):
    model = LikedItem
    extra = 0


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline, LikedItemInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
