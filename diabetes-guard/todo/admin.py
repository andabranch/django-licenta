from django.contrib import admin
from .models import Data, Diabetes

# Register your models here.

class DataAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'polyuria', 'hypotonic_urine', 'thirst','serum_osmolality','serum_sodium','diagnosis')

class DiabetesAdmin(admin.ModelAdmin):
    list_display = ('name', 'pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree_function', 'age', 'outcome')

admin.site.register(Data, DataAdmin)
admin.site.register(Diabetes, DiabetesAdmin)
