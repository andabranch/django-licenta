from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DataForm, DiabetesForm, EditForm, EditDiabetes
from .models import Data, Diabetes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.bootstrap import FormActions
from .utils import get_decision_tree_data, get_decision_tree_model
from django.urls import reverse
from sklearn.tree import export_graphviz
from sklearn import svm
import graphviz
import joblib

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard-index')
    else:
        form = DataForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/login.html', context)


@login_required
def di_form_view(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if 'predict' in request.POST:
            if form.is_valid():
                # Perform the prediction and save the result to the database
                data = form.save()
                patient_id = data.id  # Get the ID of the saved patient
                return redirect('approve', patient_id=patient_id)  # Redirect to the approval page with the patient_id
        elif 'view-tree' in request.POST:
            if form.is_valid():
                # Redirect to the view tree page
                return redirect('dashboard-tree')
    else:
        form = DataForm()
    return render(request, 'dashboard/form_di.html', {'form': form})


@login_required
def predictions(request):
    patient_id = request.GET.get('patient_id')
    if patient_id:
        predicted_diagnosis = Data.objects.filter(pk=patient_id)
    else:
        predicted_diagnosis = Data.objects.filter(archived=False)  
    context = {
        'predicted_diagnosis': predicted_diagnosis
    }
    return render(request, 'dashboard/predictions_di.html', context)

@login_required
def predictions_diabetes(request):
    patient_id = request.GET.get('patient_id')
    if patient_id:
        predicted_diagnosis = Diabetes.objects.filter(pk=patient_id)
    else:
        predicted_diagnosis = Diabetes.objects.all()
    context = {
        'predicted_diagnosis': predicted_diagnosis
    }
    return render(request, 'dashboard/predictions_diabetes.html', context)



@login_required
def approve(request, patient_id):
    patient = get_object_or_404(Data, pk=patient_id)

    if request.method == 'POST':
        if 'approve' in request.POST:
            # Perform the approval logic and save the patient to the database
            patient.archived = False
            patient.save()
            return redirect('dashboard-predictions')  # Redirect to the all patients page after approval
        elif 'reject' in request.POST:
            # Mark the patient as rejected (e.g., set a flag)
            patient.rejected = True
            patient.save()
            return redirect('dashboard-predictions')  # Redirect to the all patients page after rejection

    return render(request, 'dashboard/approve.html', {'patient': patient})

def approve_diabetes(request, patient_id):
    try:
        patient = Diabetes.objects.get(pk=patient_id)
    except Diabetes.DoesNotExist:
        return HttpResponse("Patient does not exist.")

    if request.method == 'POST':
        # Process the approval logic
        approved = request.POST.get('approve', False)
        if approved:
            # Update patient's status or perform other actions
            patient.approved = True
            patient.save()
        return redirect('dashboard-predictions-diabetes')  # Replace 'dashboard' with your desired URL name

    context = {
        'patient': patient
    }
    return render(request, 'dashboard/approve_diabetes.html', context)


@login_required
def diabetes_form_view(request):
    if request.method == 'POST':
        form = DiabetesForm(request.POST)
        if 'predict' in request.POST:
            if form.is_valid():
                # Perform the prediction and save the result to the database
                diabetes_data = form.save()
                patient_id = diabetes_data.id  # Get the ID of the saved patient
                return redirect('approve_diabetes', patient_id=patient_id)  # Redirect to the approval page with the patient_id
    else:
        form = DiabetesForm()
    return render(request, 'dashboard/form_diabetes.html', {'form': form})

# @login_required
# def diabetes_form_view(request):
#     if request.method == 'POST':
#         form = DiabetesForm(request.POST)
#         if 'predict' in request.POST:
#             if form.is_valid():
#                 # Perform the prediction and save the result to the database
#                 diabetes_data = form.save()
#                 return redirect('dashboard-predictions-diabetes')
#     else:
#         form = DiabetesForm()
#     return render(request, 'dashboard/form_diabetes.html', {'form': form})


@login_required
def edit_patient(request, pk):
    patient = get_object_or_404(Data, pk=pk)
    if request.method == 'POST':
        form = EditForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('dashboard-predictions')
    else:
        form = EditForm(instance=patient)
    return render(request, 'dashboard/edit_patient.html', {'form': form})

@login_required
def edit_patient_diabetes(request, pk):
    patient = get_object_or_404(Diabetes, pk=pk)
    if request.method == 'POST':
        form = EditDiabetes(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('dashboard-predictions-diabetes')
    else:
        form = EditDiabetes(instance=patient)
    return render(request, 'dashboard/edit_patient_diabetes.html', {'form': form})
    
@login_required
def delete_patient(request, pk):
    patient = Data.objects.get(pk=pk)
    patient.delete()
    return redirect('dashboard-predictions')

@login_required
def delete_patient_diabetes(request, pk):
    patient = Diabetes.objects.get(pk=pk)
    patient.delete()
    return redirect('dashboard-predictions-diabetes')


@login_required
def archived_patients(request):
    archived_diagnosis = Data.objects.filter(archived=True)
    return render(request, 'dashboard/archive_di.html', {'archived_diagnosis': archived_diagnosis})
#good, done
@login_required
def archived_patients_d(request):
    archived_diagnosis = Diabetes.objects.filter(archived=True)
    return render(request, 'dashboard/archive_diabetes.html', {'archived_diagnosis': archived_diagnosis})

@login_required
def archive_patient(request, pk):
    patient = get_object_or_404(Data, pk=pk)
    patient.archived = True
    patient.save()

    all_patients = Data.objects.filter(archived=False)
    return render(request, 'dashboard/predictions_di.html', {'predicted_diagnosis': all_patients})

@login_required
def unarchive_patient(request, pk):
    patient = get_object_or_404(Data, pk=pk)
    patient.archived = False
    patient.save()

    all_patients = Data.objects.filter(archived=True)
    return render(request, 'dashboard/archive_di.html', {'archived_diagnosis': all_patients})
#diabetes
@login_required
def archive_patient_d(request, pk):
    patient = get_object_or_404(Diabetes, pk=pk)
    patient.archived = True
    patient.save()

    all_patients = Diabetes.objects.filter(archived=False)
    return render(request, 'dashboard/predictions_diabetes.html', {'predicted_diagnosis': all_patients})

@login_required
def unarchive_patient_d(request, pk):
    patient = get_object_or_404(Diabetes, pk=pk)
    patient.archived = False
    patient.save()

    all_patients = Diabetes.objects.filter(archived=True)
    return render(request, 'dashboard/archive_diabetes.html', {'archived_diagnosis': all_patients})



@login_required
def tree_view(request):
    return render(request, 'dashboard/tree.html')

@login_required
def definitions(request):
    return render(request, 'dashboard/definition.html')

@login_required
def image_extraction(request):
    return render(request, 'dashboard/image_extraction.html')

@login_required
def add_file_view(request):
    if request.method == 'POST':
        # Get the uploaded file from the request
        uploaded_file = request.FILES['file']

        # Parse the CSV data into a list of dictionaries
        data = []
        for line in uploaded_file:
            line = line.decode('utf-8').strip()
            if line:
                fields = line.split(',')
                patient = {
                    'name': fields[0],
                    'age': fields[1],
                    'polyuria': fields[2],
                    'hypotonic_urine': fields[3],
                    'thirst': fields[4],
                    'serum_osmolality': fields[5],
                    'serum_sodium': fields[6],
                }
                data.append(patient)

        # Save each patient to the database
        for patient in data:
            form = DataForm(data=patient)
            if form.is_valid():
                form.save()

        # Redirect to the predictions page
        return redirect('dashboard-predictions')

    else:
        return render(request, 'dashboard/add_file.html')

