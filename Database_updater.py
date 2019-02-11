import json
import logging
import os
import MySQLdb


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


def connect_to_database():
    with MySQLdb.connect('localhost', 'bartomeu', 'userpassword', 'db.sqlite3') as db:
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()
        print("Database version : " + data)


# Method that takes all of the user's requests and looks for upates at the Files folder.
# First checks requests that have been not started and searches them in the InProgress folder,
# the remaining processes that have started are searched in the Finished folder,
# and lastly, searches started and not finished requests in the Finished folder.
def check_processes(user):

    with MySQLdb.connect('localhost', 'Bartomeu', 'userpassword', 'db.sqlite3') as db:
        cursor = db.cursor()

    for file in enumerate(os.listdir(pathInProgress)):
        with open(str(file), 'w+') as f:
            req = json.load(f)
            sql = 'SELECT * FROM Request \
                   WHERE ID = ' + str(req.id)
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            print(results)

        except:
            print("Couldn't fetch database")
    # try:
    #     # Get all processes that have not been started yet, and compare them with
    #     # the Files/InProgress folder to update the database
    #     database_requests = Request.objects.filter(user=user).filter(status='P')
    #     for db_req in enumerate(database_requests):
    #         os.makedirs(os.path.dirname(pathInProgress + user_path), exist_ok=True)
    #         for file in enumerate(os.listdir(pathInProgress + user_path)):
    #             with open(pathInProgress + user_path + str(file), 'w') as f:
    #                 req = json.load(f)
    #                 if db_req.id == req['id']:
    #                     logging.info("Process with id: "+str(req['id'])+" was updated to: started=True")
    #                     db_req.update(status='S')
    #
    #     # Get the remaining database-processes that haven't started, and check if they have already finished
    #     database_requests = Request.objects.filter(user=user).filter(status='P')
    #     for db_req in enumerate(database_requests):
    #         os.makedirs(os.path.dirname(pathInProgress + user_path), exist_ok=True)
    #         for file in enumerate(os.listdir(pathFinish + user_path)):
    #             with open(pathFinish + user_path + file, 'w') as f:
    #                 req = json.load(f)
    #                 if db_req.id == req['id']:
    #                     logging.info("Process with id: " + str(req['id']) + " was updated to: finished=True")
    #                     db_req.update(status='F')
    #
    #     # Get all processes that have been started but have not finished, and updates them
    #     database_requests = Request.objects.filter(user=user).filter(status='S')
    #     for db_req in enumerate(database_requests):
    #         os.makedirs(os.path.dirname(pathFinish + user_path), exist_ok=True)
    #         for file in enumerate(os.listdir(pathFinish + user_path)):
    #             with open(pathFinish + user_path + file, 'w') as f:
    #                 req = json.load(f)
    #                 if db_req.id == req['id']:
    #                     logging.info("Process with id: "+str(req['id'])+" was updated to: finished=True")
    #                     db_req.update(status='F')
    #
    # except IOError:
    #     logging.fatal("There was a I/O problem updating the processes of User: " + user.user_name)


connect_to_database()
