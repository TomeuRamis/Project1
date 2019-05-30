from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import ProcessType
from .models import Request, User
from .forms import FileFieldForm
import json
import os
import logging
import datetime
import shutil


absPath = os.getcwd()
userPath = os.path.join(absPath, "app1/ProcessManager/Files/")
pathReq = "/Requests/"
pathInProgress = "/InProgress/"
pathFinish = "/Finished/"

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
                return render(request, "app1/home.html", load_user_processes(user))
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
    return render(request, "app1/home.html", load_user_processes(user))


def request_process(request):
    user = User.objects.get(user_name=request.session['username'])
    if request.method == 'POST':
        user.validate()
        form = request.POST
        type_of_process = form['type_of_process']

        # Create and save the new request to the DataBase
        r = Request(type_of_process=type_of_process,
                    date_of_creation=datetime.datetime.now(),
                    date_of_start=datetime.MINYEAR,
                    date_of_finish=datetime.MINYEAR,
                    status='P',
                    user=user)
        r.save()
        # Create the new file to store the Request
        with open(os.path.join(userPath, user.user_name, pathReq, str(r.id)+'/', str(r.id)+".json"), "w+") as f:
            json.dump({"id": r.id,
                       "type": type_of_process,
                       "date of creation": str(r.date_of_creation),
                       "date of start": None,
                       "date of finish": None,
                       "status": 'P'}, f)
        logging.info("User: "+user.user_name+" has requested a new process"
                                             " id:"+str(r.id)+", type: "+type_of_process)

        # Process files
        files = request.FILES.getlist('file_field')
        fs = FileSystemStorage()
        for f in files:
            name = fs.save(f.name, f)
            shutil.move(name, os.path.join(userPath, user.user_name, pathReq, str(r.id)+'/'))
        return render(request, "app1/home.html", load_user_processes(user))
    else:
        form1 = FileFieldForm()
        form2 = ProcessType()
        return render(request, "app1/requestProcess.html", {'form1': form1,
                                                            'form2': form2,
                                                            'error': False})


def request_successful(request):
    return render(request, "app1/requestSuccessful.html")


def load_user_processes(user):
    # it could maybe be optimized like: req=Request.obj.filter(user=user) req1 = req.filter(status= ...
    context = {'user': user,
               'pending_requests': Request.objects.filter(user=user).filter(status='P'),
               'started_requests': Request.objects.filter(user=user).filter(status='S'),
               'finished_requests': Request.objects.filter(user=user).filter(status='F')}
    return context


def post(self, request):

    form_class = FileFieldForm
    template_name = 'requestProcess.html'  # Replace with your template.
    success_url = 'requestSuccessful.html'  # Replace with your URL or reverse().

    form_class = self.get_form_class()
    form = self.get_form(form_class)
    files = request.FILES.getlist('file_field')
    if form.is_valid():
        for f in files:
            with open("prueba"+f+".txt", "w") as file:
                file.write(f)
            ...  # Do something with each file.
        return self.form_valid(form)
    else:
        return self.form_invalid(form)
