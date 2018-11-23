from django.shortcuts import render
from .forms import ProcessType
import json
import os


# Create your views here.

def index(request):
    return render(request, "app1/index.html")

def login(request):
    return render(request, "app1/login.html")

def logged(request):
    context = {"usrname": request.POST['usrname'], 
               "email": request.POST['email'],
               "password": request.POST['password']}
    return render(request, "app1/logged.html", context)

def requestprocess(request):
    if request.method == 'POST':
        form = ProcessType(request.POST)
        if form.is_valid():
            if form.cleaned_data['type_of_process'] == 'fib':
                typeofprocess = "fibonacci"

            if form.cleaned_data['type_of_process'] == 'wait':
                typeofprocess = "wait"

            f = open(os.getcwd()+"/app1/ProcessManager/Files/Requests/request", "w+")
            # Should use de id of the request saved at the database
            json.dump({"id": 0,
                       "type": typeofprocess,
                       "pid": None,
                       "started": False,
                       "finished": False}, f)
            f.close()
            return render(request, "app1/requestSuccessful.html")
        return render(request, "app1/requestProcess.html")  #an error message should be added
    else:
        form = ProcessType()
        return render(request, "app1/requestProcess.html", {'form': form})

