from django.shortcuts import render, redirect, get_object_or_404
from .forms import DataForm
from .models import Data
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.bootstrap import FormActions
from .utils import get_decision_tree_data, get_decision_tree_model
from django.urls import reverse


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
def form_view(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if 'predict' in request.POST:
            if form.is_valid():
                # Perform the prediction and save the result to the database
                data = form.save()
                return redirect('dashboard-predictions')
        elif 'view-tree' in request.POST:
            if form.is_valid():
                # Redirect to the view tree page
                return redirect('dashboard-tree')
    else:
        form = DataForm()
    return render(request, 'dashboard/form.html', {'form': form})


@login_required
def tree_view(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            # Save the data
            data = form.save()
            # Pass the data to the template
            return render(request, 'dashboard/tree.html', {'form': form, 'data': data})
    else:
        form = DataForm()
    return render(request, 'dashboard/tree.html', {'form': form})


@login_required
def definitions(request):
    return render(request, 'dashboard/definition.html')




@login_required
def predictions(request):
    patient_id = request.GET.get('patient_id')
    if patient_id:
        predicted_diagnosis = Data.objects.filter(pk=patient_id)
    else:
        predicted_diagnosis = Data.objects.all()
    context = {
        'predicted_diagnosis': predicted_diagnosis
    }
    return render(request, 'dashboard/predictions.html', context)

    
@login_required
def delete_patient(request, pk):
    patient = Data.objects.get(pk=pk)
    patient.delete()
    return redirect('dashboard-predictions')

@login_required
def edit_patient(request, pk):
    patient = get_object_or_404(Data, pk=pk)
    if request.method == 'POST':
        form = DataForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('dashboard-predictions')
    else:
        form = DataForm(instance=patient)
    return render(request, 'dashboard/edit_patient.html', {'form': form})

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

@login_required
def diabetes(request):
    return render(request, 'dashboard/diabetes.html')