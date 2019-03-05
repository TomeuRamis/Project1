from app1.models import User, Request
import json
import logging
import os


# PATH CONSTANTS
absPath = os.getcwd()
pathReq = os.path.join(absPath, "app1/ProcessManager/Files/Requests/")
pathInProgress = os.path.join(absPath, "app1/ProcessManager/Files/InProgress/")
pathFinish = os.path.join(absPath, "/app1/ProcessManager/Files/Finished/")

# Logging configuration
logging.basicConfig(filename='web_page.log',
                    level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')


def check_processes(user):

    try:
        user = User.objects.get(user=user)
        # Get all processes that have not been started yet, and compare them with
        # the Files/InProgress folder to update the database
        database_requests = Request.objects.filter(user=user).filter(status='P')
        for db_req in enumerate(database_requests):
            for file in enumerate(os.listdir(pathInProgress)):
                with open(pathInProgress + str(file), 'w') as f:
                    req = json.load(f)
                    if db_req.id == req['id']:
                        print("hello")

    except IOError:
        logging.fatal("There was a I/O problem updating the processes of User: " + user.user_name)



upd_db()