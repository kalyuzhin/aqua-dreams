from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html
from .models import Pool, PoolImage, PoolDescription


class PoolImageFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        image_count = sum(
            1 for form in self.forms
            if form.cleaned_data
            and not form.cleaned_data.get('DELETE', False)
            and form.cleaned_data.get('image')
        )
        if image_count > 6:
            raise ValidationError("Можно загрузить максимум 6 изображений!")


class PoolImageInline(admin.TabularInline):
    model = PoolImage
    formset = PoolImageFormSet
    extra = 1
    max_num = 6
    fields = ('image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="100" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = "Превью"


class PoolDescriptionInline(admin.StackedInline):
    model = PoolDescription
    extra = 0
    max_num = 1
    min_num = 1
    validate_min = True
    fields = ('description',)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['description'].required = True
        return formset


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'main_image_preview', 'short_description_preview')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [PoolDescriptionInline, PoolImageInline]
    readonly_fields = ('main_image_preview',)

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" height="50" />', obj.main_image.url)
        return "Нет изображения"

    main_image_preview.short_description = "Превью"

    def short_description_preview(self, obj):
        return obj.description_short[:100] + '...' if obj.description_short else "—"

    short_description_preview.short_description = "Краткое описание"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('images', 'description_obj')