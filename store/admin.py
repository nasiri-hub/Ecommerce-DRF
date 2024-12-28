from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.db.models import Count, F
from django.http import HttpRequest
from django.utils.html import format_html
from django.urls import reverse
from urllib.parse import urlencode
from .models import Product, Collection, Customer, Order, OrderItem, Cart, CartItem, ProductImage


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


class ProductImageInline(admin.TabularInline):
    extra = 0
    model = ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance: ProductImage):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"')
        return ''


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    inlines = [ProductImageInline]
    prepopulated_fields = {
        'slug': ['title']
    }
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    date_hierarchy = 'last_update'
    ordering = ['title']
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self, product: Product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products where successfully updated.',
            messages.ERROR
        )

    class Media:
        css = {
            'all': ['store/styles.css']
        }


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection: Collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({
                   'collection_id': str(collection.id)
               }))
        return format_html(f'<a href="{url}">{collection.products_count}</a>')

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(products_count=Count('products'))


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['user__first_name', 'user__last_name']
    list_select_related = ['user']
    search_fields = ['user__first_name__istartswith',
                     'user__last_name__istartswith']

    def orders(self, customer: Customer):
        url = (reverse('admin:store_order_changelist') +
               '?' +
               urlencode({
                   'customer_id': str(customer.id)
               }))

        return format_html(f'<a href="{url}">{customer.orders}</a>')

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(orders=Count('order'))


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    extra = 1
    max_num = 9
    min_num = 1
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    date_hierarchy = 'placed_at'
    inlines = [OrderItemInline]
    list_editable = ['payment_status']
    list_display = ['placed_at', 'payment_status', 'customer']
    list_per_page = 10
    ordering = ['payment_status']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'product__title',
                    'unit_price', 'quantity', 'best_seller']

    @admin.display(ordering='best_seller')
    def best_seller(self, orderitem: OrderItem):
        if orderitem.best_seller > 300:
            return 'Best Seller'
        return orderitem.best_seller

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(best_seller=F('unit_price') * F('quantity')).filter(best_seller__gt=200)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity']
