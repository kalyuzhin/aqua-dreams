from django.contrib import admin
from .models import Project, ProjectDetail, ProjectCategory, ProjectCategoryImages
from django.core.exceptions import ValidationError
from django.forms import ModelForm


class ProjectDetailForm(ModelForm):
    class Meta:
        model = ProjectDetail
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        for field_name, field_value in cleaned_data.items():
            if field_name == 'id':
                continue
            if field_value in (None, ''):
                raise ValidationError(f"Поле {field_name} обязательно для заполнения")
        return cleaned_data


class ProjectDetailInline(admin.TabularInline):
    model = ProjectDetail
    form = ProjectDetailForm
    extra = 1
    max_num = 6

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.validate_max = True
        return formset


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectDetailInline]
    list_display = ['title', 'address', 'is_flipped']
    search_fields = ['title', 'address']

    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            if formset.model == ProjectDetail and len(formset.forms) > 6:
                raise ValidationError("Нельзя добавить более 6 ProjectDetails")
        super().save_related(request, form, formsets, change)


class ProjectCategoryImagesInline(admin.TabularInline):
    model = ProjectCategoryImages
    extra = 1
    readonly_fields = ['image_thumbnail']

    def image_thumbnail(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="80" />'
        return "-"

    image_thumbnail.short_description = "Image"
    image_thumbnail.allow_tags = True


class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at', 'deleted_at']
    search_fields = ['name']
    inlines = [ProjectCategoryImagesInline]


class ProjectCategoryImagesAdmin(admin.ModelAdmin):
    list_display = ['category', 'image_display']
    search_fields = ['category__name']
    readonly_fields = ['image_display']

    def image_display(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="80" />'
        return "-"

    image_display.short_description = "Image"
    image_display.allow_tags = True


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(ProjectCategoryImages, ProjectCategoryImagesAdmin)
