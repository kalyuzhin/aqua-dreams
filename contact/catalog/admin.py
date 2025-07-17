from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html
from django.forms import ModelForm
from .models import Category, Product, ProductImage, Specification

MAX_CATEGORIES = 5
MAX_IMAGES = 6
MIN_IMAGES = 3
MAX_SPECS = 2

class CategoryForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        if Category.objects.count() >= MAX_CATEGORIES and not self.instance.pk:
            raise ValidationError(f"Можно создать максимум {MAX_CATEGORIES} категорий!")
        return cleaned_data

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    form = CategoryForm

    def has_add_permission(self, request):
        return Category.objects.count() < MAX_CATEGORIES

class ProductImageFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        image_count = sum(
            1 for form in self.forms
            if form.cleaned_data
            and not form.cleaned_data.get('DELETE', False)
            and form.cleaned_data.get('image')
        )

        if image_count < MIN_IMAGES:
            raise ValidationError(f"Минимум {MIN_IMAGES} изображения обязательно!")
        if image_count > MAX_IMAGES:
            raise ValidationError(f"Максимум {MAX_IMAGES} изображений разрешено!")

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if not form.cleaned_data.get('image'):
                    raise ValidationError("Все изображения должны быть заполнены.")

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    formset = ProductImageFormSet
    extra = 1
    max_num = MAX_IMAGES
    fields = ('image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="100" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = "Превью"

class SpecificationFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        valid_forms = [
            form for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
        ]
        if len(valid_forms) != MAX_SPECS:
            raise ValidationError(f"Должно быть ровно {MAX_SPECS} характеристики!")

        for form in valid_forms:
            if not form.cleaned_data.get('key') or not form.cleaned_data.get('value'):
                raise ValidationError("Все характеристики должны быть заполнены.")

class SpecificationInline(admin.TabularInline):
    model = Specification
    formset = SpecificationFormSet
    extra = MAX_SPECS
    max_num = MAX_SPECS
    fields = ('key', 'value')
    verbose_name_plural = "Характеристики"

    def get_formset(self, request, obj=None, **kwargs):
        if obj and obj.specifications.exists():
            self.extra = 0
        return super().get_formset(request, obj, **kwargs)

class ProductForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['category', 'name', 'slug', 'reliability_text', 'special_notes', 'image', 'image_second']
        for field in required_fields:
            if not cleaned_data.get(field):
                raise ValidationError(f"Поле '{field}' обязательно для заполнения.")
        return cleaned_data

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'main_image_preview', 'second_image_preview', 'popularity')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SpecificationInline, ProductImageInline]
    readonly_fields = ('main_image_preview', 'second_image_preview')
    list_filter = ('category', 'popularity')
    search_fields = ('name', 'category__name')
    form = ProductForm
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'popularity', 'reliability_text', 'special_notes')
        }),
        ('Изображения продукта', {
            'fields': (
                ('image', 'main_image_preview'),
                ('image_second', 'second_image_preview')
            ),
            'classes': ('collapse', 'closed')
        }),
    )

    def main_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" />', obj.image.url)
        return "Нет изображения"

    main_image_preview.short_description = "Превью (основное)"

    def second_image_preview(self, obj):
        if obj.image_second:
            return format_html('<img src="{}" height="50" />', obj.image_second.url)
        return "Нет изображения"

    second_image_preview.short_description = "Превью (дополнительное)"