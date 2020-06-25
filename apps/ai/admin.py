from django.contrib import admin

from apps.ai.models.ModelTraining import ModelTraining
from apps.ai.models.SklearnParameters import SklearnParameters

# Register your models here.
class SklearnParametersInline(admin.TabularInline):
    model = SklearnParameters


class ModelTrainingAdmin(admin.ModelAdmin):
    inlines = [SklearnParametersInline]
admin.site.register(ModelTraining, ModelTrainingAdmin)