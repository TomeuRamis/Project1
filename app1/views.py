from django.shortcuts import render
from .forms import ProcessType
from .models import Request, User
import json
import os


# Create your views here.



def index(request):
    return render(request, "app1/index.html")


def login(request):
    if request.method == 'POST':
        user = User.objects.get(user_name=request.POST['usrname'])
        if user == User.objects.get(email=request.POST['email']):
            context = {"user": user,
                       "requests": Request.objects.filter(user=user)}
            return render(request, "app1/logged.html", context)
        else:
            return render(request, "app1/loginFailed.html")
    else:
        return render(request, "app1/login.html")


def logged(request):
    user = {"usrname": request.POST['usrname'],
            "email": request.POST['email']}
    requests = Request.objects.all()
    context = {"user": user,
               "requests": requests}
    return render(request, "app1/logged.html", context)


def requestprocess(request):
    if request.method == 'POST':
        user = User.objects.get(user_name=request.POST['user'])
        form = ProcessType(request.POST)
        if form.is_valid():
            type_of_process = form.cleaned_data['type_of_process']
            # Create and save the new request to the DataBase
            r = Request(type_of_process=type_of_process, user=user)
            r.save()
            # Create the new file to store the Request
            f = open(os.getcwd()+"/app1/ProcessManager/Files/Requests/request"+str(r.id), "w+")
            json.dump({"id": r.id,
                       "type": type_of_process,
                       "date of creation": str(r.date_of_creation),
                       "pid": -1,
                       "started": False,
                       "finished": False}, f)
            f.close()
            return render(request, "app1/requestSuccessful.html", {'user': user})
        else:
            form = ProcessType()
            return render(request, "app1/requestProcess.html", {'form': form,
                                                                'error': True,
                                                                'user': user})
    else:
        form = ProcessType()
        return render(request, "app1/requestProcess.html", {'form': form,
                                                            'error': False,
                                                            'user': request.GET['user']})


def request_successful(request):
    if request.method == 'GET':
        if request.GET['back_to_main']:
            return render(request, , {'user': request.GET['usr']})
        else:
            return render(request, "app1/requestProcess.html", {'user': request.GET['user']})
