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


def check_processes():

    try:
        # Update database with the file system
        files_to_delete = []
        for file in enumerate(os.listdir(pathInProgress)):
            with open(pathInProgress + str(file), 'w') as f:
                req = json.load(f)
                try:
                    db_req = Request.objects.filter(id=req['id'])
                    if not db_req.status == 'S' :
                        req['status'] = 'F'
                        with open(pathFinish, 'w') as g:
                            json.dump(req)
                        files_to_delete.append(file)

                except Request.DoesNotExist:
                    req['status'] = 'E'  # ERROR

        for fi in files_to_delete:
            os.remove(fi)

    except IOError:
        logging.fatal("There was a I/O problem updating the processes of User: " + user.user_name)
