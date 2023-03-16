from django.urls import path 
from .import views 
from django.contrib.auth import views as auth_views
from .views import form_view, predictions, delete_patient, edit_patient,definitions, tree_view


urlpatterns = [
  path('', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
  path('form/',views.form_view, name="dashboard-index"),
  path('predictions/',views.predictions, name="dashboard-predictions"),
  path('delete_patient/<int:pk>', delete_patient, name='delete_patient'),
  path('edit_patient/<int:pk>', edit_patient, name='edit_patient'),
  path('definitions/', views.definitions, name="definitions"),
  path('tree/', views.tree_view, name='dashboard-tree'), 

]
