from django.urls import path 
from .import views 
from django.contrib.auth import views as auth_views
from .views import delete_patient_diabetes, di_form_view, edit_patient_diabetes, predictions, delete_patient, edit_patient,definitions, add_file_view,diabetes_form_view, predictions_diabetes,image_extraction, archived_patients, archive_patient, unarchive_patient, approve,archived_patients_d,archive_patient_d,unarchive_patient_d

urlpatterns = [
  path('', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
  path('form/',views.di_form_view, name="dashboard-index"),
  path('form-diabetes/', views.diabetes_form_view, name='dashboard-diabetes'),
  path('predictions-di/',views.predictions, name="dashboard-predictions"),
  path('predictions-diabetes/', views.predictions_diabetes, name='dashboard-predictions-diabetes'),
  path('add-file/', views.add_file_view, name='dashboard-add-file'),
  path('image-extraction/', views.image_extraction, name='image-extraction'),
  path('delete_patient/<int:pk>', delete_patient, name='delete_patient'),
  path('delete_patient_diabetes/<int:pk>', delete_patient_diabetes, name='delete_patient_diabetes'),

  path('edit_patient/<int:pk>', edit_patient, name='edit_patient'),
  path('tree/', views.tree_view, name='dashboard-tree'),
  path('definitions/', views.definitions, name="definitions"),
  path('archive-di/', views.archived_patients, name='archived_patients'),
  path('archive-patient/<int:pk>/', views.archive_patient, name='archive_patient'),
  path('unarchive-patient/<int:pk>/', views.unarchive_patient, name='unarchive_patient'),
#diabetes
  path('archive-diabetes/', views.archived_patients_d, name='archived_patients_d'),

  path('archive-patient-d/<int:pk>/', views.archive_patient_d, name='archive_patient_d'),
  path('unarchive-patient-d/<int:pk>/', views.unarchive_patient_d, name='unarchive_patient_d'),


  path('edit_patient_diabetes/<int:pk>', edit_patient_diabetes, name='edit_patient_diabetes'),


  path('approve/<int:patient_id>/', approve, name='approve'),
  path('approve-diabetes/<int:patient_id>/', views.approve_diabetes, name='approve_diabetes'),


  # path('accept/', views.accept_diagnosis, name='accept_diagnosis'),


]
