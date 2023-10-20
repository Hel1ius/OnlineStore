from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models


class CharacteristicsInline(admin.TabularInline):
    model = models.CharacteristicsProduct
    extra = 1


class ReviewInline(admin.TabularInline):
    model = models.Reviews
    extra = 1
    readonly_fields = ('name', 'email')


class ProductImagesInline(admin.TabularInline):
    model = models.ProductImages
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="150"')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'manufacturer', 'quantity', 'is_new', 'is_on_sale',
                    'is_hit', 'draft')
    list_filter = ('category', 'manufacturer', 'is_on_sale', 'is_hit', 'draft')
    search_fields = ('category__name', 'name')
    inlines = [CharacteristicsInline, ProductImagesInline, ReviewInline]
    readonly_fields = ('url', 'get_image')
    save_on_top = True
    list_editable = ('draft',)
    fields = (('name', 'description', 'get_image', 'preview'), ('category', 'manufacturer'), ('price', 'quantity', 'is_new'),
              ('sale_price', 'is_on_sale', 'is_hit'))

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.preview.url} width="150" height="150"')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('name',)


@admin.register(models.Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'product')
    readonly_fields = ('name', 'email')


@admin.register(models.ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('product', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="50"')


admin.site.register(models.Manufacturer)
admin.site.register(models.Order)
admin.site.register(models.FavoriteProduct)
admin.site.register(models.RatingStar)
admin.site.register(models.Rating)
