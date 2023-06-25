from django import forms
from .models import Data, Diabetes

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['name', 'age', 'polyuria', 'hypotonic_urine', 'thirst', 'serum_osmolality', 'serum_sodium']

class DiabetesForm(forms.ModelForm):
    class Meta:
        model = Diabetes
        fields = ['name', 'pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree_function', 'age']

class EditForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['name', 'age', 'polyuria', 'hypotonic_urine', 'thirst', 'serum_osmolality', 'serum_sodium', 'diagnosis']

class EditDiabetes(forms.ModelForm):
    class Meta:
        model = Diabetes
        fields = ['name', 'pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree_function', 'age', 'outcome']