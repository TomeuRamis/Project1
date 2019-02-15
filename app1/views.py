from django.shortcuts import render
from .forms import ProcessType
from .models import Request, User
import json
import os
import logging


absPath = os.getcwd()
pathReq = os.path.join(absPath, "app1/ProcessManager/Files/Requests/")
pathInProgress = os.path.join(absPath, "app1/ProcessManager/Files/InProgress/")
pathFinish = os.path.join(absPath, "/app1/ProcessManager/Files/Finished/")

logging.basicConfig(filename='web_page.log',
                    level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')


# Create your views here.

def index(request):
    return render(request, "app1/index.html")


def login(request):
    if request.method == 'POST':
        context = {'user': None,
                   'access': True}
        try:
            user = User.objects.get(user_name=request.POST['username'])
            if user == User.objects.get(email=request.POST['email']):
                request.session['username'] = user.user_name
                request.session['email'] = user.email
                context['user'] = user
                logging.info('User: ' + user.user_name + ' has logged in.')
                return render(request, "app1/home.html", context)
            else:
                logging.error('User: ' + user.user_name + ' has tried to log in with'
                                                          ' a wrong email ( ' + request.POST['email'] + ' ).')
                context['access'] = False   # Deny access to the web-page
                return render(request, "app1/login.html", context)
        except User.DoesNotExist:
            logging.error('There was an attempt to log in with the wrong credentials '
                          'user name: ' + request.POST['username'] + ', email: ' + request.POST['email'])
            context['access'] = False       # Deny access to the web-page
            return render(request, "app1/login.html", context)
    else:
        return render(request, "app1/login.html")


# Load home page and update Request database
def logged(request):

    user = User.objects.get(user_name=request.session['username'])
    # it could maybe be optimized like: req=Request.obj.filter(user=user) req1 = req.filter(status= ...
    context = {'user': user,
               'pending_requests': Request.objects.filter(user=user).filter(status='P'),
               'started_requests': Request.objects.filter(user=user).filter(status='S'),
               'finished_requests': Request.objects.filter(user=user).filter(status='F')}
    return render(request, "app1/home.html", context)


def request_process(request):
    user = User.objects.get(user_name=request.session['username'])
    if request.method == 'POST':
        form = ProcessType(request.POST)
        if form.is_valid():
            type_of_process = form.cleaned_data['type_of_process']
            # Create and save the new request to the DataBase
            r = Request(type_of_process=type_of_process, user=user)
            r.save()
            # Create the new file to store the Request
            with open(os.path.join(pathReq, "request"+str(r.id)+".json"), "w+") as f:
                json.dump({"id": r.id,
                           "type": type_of_process,
                           "date of creation": str(r.date_of_creation),
                           "pid": -1,
                           "status": 'P'}, f)
            logging.info("User: "+user.user_name+" has requested a new process"
                                                 " id:"+str(r.id)+", type: "+type_of_process)
            return render(request, "app1/requestSuccessful.html")
        else:
            logging.fatal("User: " + user.user_name + " tried to request a process but was an error validating the form")
            form = ProcessType()
            return render(request, "app1/requestProcess.html", {'form': form,
                                                                'error': True})
    else:
        form = ProcessType()
        return render(request, "app1/requestProcess.html", {'form': form,
                                                            'error': False})


def request_successful(request):
    return render(request, "app1/requestSuccessful.html")
