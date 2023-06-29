from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DataForm, DiabetesForm, EditForm, EditDiabetes
from .models import Data, Diabetes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
                # perform pred and save to db
                data = form.save()
                patient_id = data.id  # get id
                return redirect('approve', patient_id=patient_id) 
        elif 'view-tree' in request.POST:
            if form.is_valid():
                data = form.save()  
                patient_id = data.id  
                return redirect('tree_view', patient_id=patient_id)
    else:
        form = DataForm()
    return render(request, 'dashboard/form_di.html', {'form': form})

@login_required
def diabetes_form_view(request):
    if request.method == 'POST':
        form = DiabetesForm(request.POST)
        if 'predict' in request.POST:
            if form.is_valid():
                diabetes_data = form.save()
                patient_id = diabetes_data.id  
                return redirect('approve_diabetes', patient_id=patient_id) 
    else:
        form = DiabetesForm()
    return render(request, 'dashboard/form_diabetes.html', {'form': form})


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
            #perform approval logic
            patient.archived = False
            patient.save()
            return redirect('dashboard-predictions')  
        elif 'reject' in request.POST:
            #mark patient as rejected
            patient.rejected = True
            patient.save()
            return redirect('dashboard-predictions') 
    return render(request, 'dashboard/approve.html', {'patient': patient})

def approve_diabetes(request, patient_id):
    try:
        patient = Diabetes.objects.get(pk=patient_id)
    except Diabetes.DoesNotExist:
        return HttpResponse("Patient does not exist.")

    if request.method == 'POST':
        approved = request.POST.get('approve', False)
        if approved:
            patient.approved = True
            patient.save()
        return redirect('dashboard-predictions-diabetes') 

    context = {
        'patient': patient
    }
    return render(request, 'dashboard/approve_diabetes.html', context)


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


#archived pages
@login_required
def archived_patients(request):
    archived_diagnosis = Data.objects.filter(archived=True)
    return render(request, 'dashboard/archive_di.html', {'archived_diagnosis': archived_diagnosis})

@login_required
def archived_patients_d(request):
    archived_diagnosis = Diabetes.objects.filter(archived=True)
    return render(request, 'dashboard/archive_diabetes.html', {'archived_diagnosis': archived_diagnosis})


#archive ability
@login_required
def archive_patient(request, pk):
    patient = get_object_or_404(Data, pk=pk)
    patient.archived = True
    patient.save()
    all_patients = Data.objects.filter(archived=False)
    return render(request, 'dashboard/predictions_di.html', {'predicted_diagnosis': all_patients})

@login_required
def archive_patient_d(request, pk):
    patient = get_object_or_404(Diabetes, pk=pk)
    patient.archived = True
    patient.save()
    all_patients = Diabetes.objects.filter(archived=False)
    return render(request, 'dashboard/predictions_diabetes.html', {'predicted_diagnosis': all_patients})


#unarchive ability
@login_required
def unarchive_patient(request, pk):
    patient = get_object_or_404(Data, pk=pk)
    patient.archived = False
    patient.save()
    all_patients = Data.objects.filter(archived=True)
    return render(request, 'dashboard/archive_di.html', {'archived_diagnosis': all_patients})

@login_required
def unarchive_patient_d(request, pk):
    patient = get_object_or_404(Diabetes, pk=pk)
    patient.archived = False
    patient.save()
    all_patients = Diabetes.objects.filter(archived=True)
    return render(request, 'dashboard/archive_diabetes.html', {'archived_diagnosis': all_patients})


@login_required
def tree_view(request, patient_id):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            data = form.save()
            patient_id = data.id 
            return redirect('dashboard-predictions', patient_id=patient_id) 
    else:
        form = DataForm()
    return render(request, 'dashboard/tree.html', {'form': form})


@login_required
def definitions(request):
    return render(request, 'dashboard/definition.html')



@login_required
def add_file_view(request):
    if request.method == 'POST':
        # get uploaded file from the req
        uploaded_file = request.FILES['file']
        # csv data into list of dicts
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
        # save each patient to db
        for patient in data:
            form = DataForm(data=patient)
            if form.is_valid():
                form.save()
        return redirect('dashboard-predictions')

    else:
        return render(request, 'dashboard/add_file.html')




import base64

import numpy as np
import pytesseract
from django.contrib import messages
from django.shortcuts import render
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"  
)


import base64
import pytesseract
import numpy as np
from PIL import Image

from django.shortcuts import render


def image_extraction(request):
    if request.method == "POST":
        try:
            image = request.FILES["imagefile"]
            # encode img to base64 string
            image_base64 = base64.b64encode(image.read()).decode("utf-8")
        except:
            messages.add_message(
                request, messages.ERROR, "No image selected or uploaded"
            )
            return render(request, "img_extraction.html")
        lang = request.POST["language"]
        img = np.array(Image.open(image))
        text = pytesseract.image_to_string(img, lang=lang)
        # return text to html
        return render(request, "dashboard/img_extraction.html", {"ocr": text, "image": image_base64})

    return render(request, "dashboard/img_extraction.html")



