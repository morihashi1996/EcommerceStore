from django.contrib import admin
from .models import Category, Product, Images


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'in_stock', 'created', 'updated', 'image']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline]
