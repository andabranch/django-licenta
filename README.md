# Medical diagnosis Web Application

## Overview

The aim of this application is to provide a precise diagnosis that strengthens any doctor’sknowledge. The misdiagnosis of diabetes insipidus and related diseases is very common and can lead to serious effects that can  put the patient in a coma.

I created this web application in Django and I am using a ML model based on decision rules of polyuria, hypotonic urine, thirst, serum osmolality and serum sodium. Once the patient's data is introduced, the user can simply see the predicted diagnosis or he can choose to visualize the result in a decision tree that is dinamically built. Then the data is saved in a database where the doctor can see all his patients. From the UI the doctor can also add, edit, delete, archive a patient and approve of the diagnosis. When the diagnosis is approved or a patient is archived, the certain data is then used to improve the accuracy of the predictions.


## Installation 
1. The first step towards running this web application is to install an IDE such as Visual Studio Code, which can be found here:
```bash
https://code.visualstudio.com/
```
2. Download the code and dependencies named requirements.txt from this repository and unzip the folder. 

![image](https://user-images.githubusercontent.com/107280183/226911715-c8f28446-7450-46b1-b73f-f902291e42fc.png)


3. Open the folder in Visual Studio Code and open a Terminal in which you will write the following command in order to install the dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```

4. In the Terminal, run the following command in order for the application to start:
```bash
python manage.py runserver
```

# UI
The login page:

![image](https://user-images.githubusercontent.com/107280183/226926087-1230edf3-4f33-4297-a941-a59692aee238.png)

The form page, where the patient's data gets inputed in order to get a prediction:

![image](https://github.com/raepmi/django-licenta/assets/107280183/c6211d36-9bbd-4050-ab26-1c465e437b67)

This is the all active patients page, where the user can delete, edit and archeive a pacient:

![image](https://github.com/raepmi/django-licenta/assets/107280183/856423c1-b9ff-42c6-854c-02655b39db45)

Archived Patients page:

![image](https://github.com/raepmi/django-licenta/assets/107280183/4792d223-39ce-49ac-b2c4-5ed2d254f156)


Image extraction page for blood tests:

![image](https://github.com/raepmi/django-licenta/assets/107280183/914de9f1-29a7-4d8d-975b-63cb649a9622)
