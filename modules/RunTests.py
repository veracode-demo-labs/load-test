import subprocess
import json
import time
from threading import Semaphore, Thread

# Creates scan request 
def execute_shell_script(user, semaphore_dict, execution_count):

    print(f"Executing with user {user['user_id']} - Execution: {execution_count}")
    
    print(f"Executing with user {user['user_id']} - Execution: {execution_count}")

    # Use the user to run the pipeline scan on verademo-dotnet
    command = ["java", "-jar", "resources/pipeline-scan.jar", "-vid", user["api_id"], "-vkey", user["api_secret"], "-f", "resources/Verademo-dotnet.zip", "-jf", f"resultExec{execution_count}.json"]

    subprocess.call(command)
    
    user["executions"] = user.get("executions", 0) - 1
    
    # Task is done, allow another thread
    semaphore_dict[user["user_id"]].release()

# This goes through adding threads for each user up to 5 to run 'execute_shell_script' 
def control_execution(users, semaphore_dict, total_executions):
    execution_count = 0

    while execution_count < total_executions:
        # Add 
        for user in users:
            if execution_count >= total_executions:
                break
            # Checks if there are 5 executions
            if user.get("executions", 0) < 5 and semaphore_dict[user["user_id"]].acquire(blocking=False):
                thread = Thread(target=execute_shell_script, args=(user, semaphore_dict, execution_count))
                thread.start()

                execution_count += 1

        time.sleep(1)

def run_tests(total_executions):

    # Load in data from json file
    with open("outputs/UsersAPIs.json", "r") as file:
        data = json.load(file)
        users = data["users"]

    # declares each user to get max 5 threads.
    semaphore_dict = {user["user_id"]: Semaphore(5) for user in users}

    control_execution(users, semaphore_dict, total_executions)
