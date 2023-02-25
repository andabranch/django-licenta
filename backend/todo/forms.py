from django import forms
from .models import Data 

class DataForm(forms.ModelForm):
  class Meta:
    model = Data
    fields = ['name','age','polyuria','hypotonic_urine','thirst','serum_osmolality','serum_sodium']