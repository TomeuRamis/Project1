from django.shortcuts import render
from .forms import ProcessType
from .models import Request, User
import json
import os
import logging


absPath = os.getcwd()
pathReq = absPath + "ProcessManager/Files/Requests/"
pathInProgress = absPath + "ProcessManager/Files/InProgress/"
pathFinish = absPath + "ProcessManager/Files/Finished/"

logging.basicConfig(filename='process_manager.log',
                    level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')


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
                logging.info('User: ' + user.user_name + ' has logged in.')
                return render(request, "app1/login.html", context)
            else:
                logging.error('User: ' + user.user_name + ' has tried to log in with'
                                                          ' a wrong email ( ' + request.POST['email'] + ' ).')
                return render(request, "app1/loginFailed.html")
        except User.DoesNotExist:
            logging.error('There was an attempt to log in with the wrong credentials '
                          'user name: ' + request.POST['username'] + ', email: ' + request.POST['email'])
            return render(request, "app1/loginFailed.html")
    else:
        return render(request, "app1/login.html")


# Load home page and update Request database
def logged(request):

    user = User.objects.get(user_name=request.session['username'])
    check_processes(user)
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
            f = open(pathReq + request.session['username'] + "/request" + str(r.id), "w+")
            json.dump({"id": r.id,
                       "type": type_of_process,
                       "date of creation": str(r.date_of_creation),
                       "pid": -1,
                       "started": False,
                       "finished": False}, f)
            f.close()
            logging.info("User: "+user.user_name+" has requested a new process"
                                                 " [id:"+r.id+", type: "+type_of_process)
            return render(request, "app1/requestSuccessful.html", {'user': user})
        else:
            logging.fatal("User: " + user.user_name + " tried to request a process but was an error validating the form")
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


# Method that takes all of the user's requests and looks for upates at the Files folder.
# First checks requests that have been not started and searches them in the InProgress folder,
# the remaining processes that have started are searched in the Finished folder,
# and lastly, searches started and not finished requests in the Finished folder.
def check_processes(user):
    user_path = user['user_name'] + '/'

    try:
        # Get all processes that have not been started yet, and compare them with
        # the Files/InProgress folder to update the database
        database_requests = Request.objets.filter(user=user).filter(started=False)
        for db_req in enumerate(database_requests):
            for file in enumerate(os.listdir(pathInProgress + user_path)):
                f = open(pathInProgress + user_path + file, 'r')
                req = json.load(f)
                if db_req['pk'] == req['id']:
                    logging.info("Process with id: "+req['id']+" was updated to: started=True")
                    db_req.update(started=True)

        # Get the remaining database-processes that haven't started, and check if they have already finished
        database_requests = Request.objets.filter(user=user).filter(started=False)
        for db_req in enumerate(database_requests):
            for file in enumerate(os.listdir(pathFinish + user_path)):
                f = open(pathInProgress + user_path + file, 'r')
                req = json.load(f)
                if db_req['pk'] == req['id']:
                    logging.info("Process with id: "+req['id']+" was updated to: finished=True")
                    db_req.update(finished=True)

        # Get all processes that have been started but have not finished, and updates them
        database_requests = Request.objets.filter(user=user).filter(started=True).filter(finished=False)
        for db_req in enumerate(database_requests):
            for file in enumerate(os.listdir(pathFinish + user_path)):
                f = open(pathInProgress + user_path + file, 'r')
                req = json.load(f)
                if db_req['pk'] == req['id']:
                    logging.info("Process with id: "+req['id']+" was updated to: finished=True")
                    db_req.update(finished=True)

    except IOError:
        logging.fatal("There was a I/O problem updating the processes of User: " + user.user_name)
        print("I/O error")
