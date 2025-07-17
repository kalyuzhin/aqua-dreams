from django.contrib import admin
from .models import Project, ProjectDetail
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


admin.site.register(Project, ProjectAdmin)