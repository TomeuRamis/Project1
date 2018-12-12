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
        try:
            user = User.objects.get(user_name=request.POST['username'])
            if user == User.objects.get(email=request.POST['email']):
                request.session['username'] = user.user_name
                request.session['email'] = user.email
                context = {'user': user,
                           'access': True}
                return render(request, "app1/login.html", context)
            else:
                return render(request, "app1/loginFailed.html")
        except User.DoesNotExist:
            return render(request, "app1/loginFailed.html")
    else:
        return render(request, "app1/login.html")


def logged(request):
    user = User.objects.get(user_name=request.session['username'])
    requests = Request.objects.filter(user=user)
    context = {'user': user,
               'requests': requests}
    return render(request, "app1/logged.html", context)


def requestprocess(request):
    user = User.objects.get(user_name=request.session['username'])
    if request.method == 'POST':
        form = ProcessType(request.POST)
        if form.is_valid():
            type_of_process = form.cleaned_data['type_of_process']
            # Create and save the new request to the DataBase
            r = Request(type_of_process=type_of_process, user=user)
            r.save()
            # Create the new file to store the Request
            f = open(os.getcwd() + "/app1/ProcessManager/Files/Requests/request" + str(r.id), "w+")
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
                                                            'user': user})


def request_successful(request):
    user = User.objects.get(user_name=request.session['username'])
    if request.method == 'GET':
        if request.GET['back_to_main']:
            return render(request, "app1/logged.html",
                          {'user': user,
                           'requests': Request.objects.filter(user=user)})
        else:
            return render(request,
                          "app1/requestProcess.html",
                          {'user': user})


absPath = os.getcwd()
pathReq = absPath + "/Files/Requests/"
pathInProgress = absPath + "/Files/InProgress/"
pathFinish = absPath + "/Files/Finished/"


# Look at the Files folder to update the user's requests
def check_processes(user):
    try:
        for i, file in enumerate(os.listdir(pathInProgress)):
            f = open(pathInProgress + file, 'r')
            request = json.load(f)
            database_request = Request.objets.get(request['id'])

    except IOError:
        print("IO error")
    except Request.DoesNotExist:
        print("The process with id: " + i + " was not found on the Data Base")
