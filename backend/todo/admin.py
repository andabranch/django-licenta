from django.contrib import admin
from .models import Data
# Register your models here.

class DataAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'polyuria', 'hypotonic_urine', 'thirst','serum_osmolality','serum_sodium','diagnosis')

admin.site.register(Data, DataAdmin)