from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from sklearn.tree import DecisionTreeClassifier
import joblib



thirst_choices=[(0,"absent to low"),
(1, "excessive")]

class Data(models.Model):
  name=models.CharField(max_length=50, null=True)
  age=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(140)],null=True)
  polyuria=models.PositiveIntegerField(validators=[MaxValueValidator(1000)],null=True)
  hypotonic_urine=models.FloatField(validators=[MaxValueValidator(5)],null=True)
  thirst=models.PositiveIntegerField(choices=thirst_choices, null=True)
  serum_osmolality=models.PositiveIntegerField(validators=[MaxValueValidator(500)],null=True)
  serum_sodium=models.PositiveIntegerField(validators=[MaxValueValidator(500)],null=True)
  diagnosis=models.CharField(max_length=30, blank=True)
  date=models.DateTimeField(auto_now_add=True)

#override default save to database 
  def save(self, *args, **kwargs):
    model=joblib.load('ml_model/di_recommender.joblib')
    self.diagnosis = model.predict([[ self.age, self.polyuria, self.hypotonic_urine, self.thirst,self.serum_osmolality,self.serum_sodium ]])
    return super().save(*args, **kwargs)

  class Meta:
    ordering=['-date']

  def __str__(self) -> str:
    return self.name