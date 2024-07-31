import subprocess
import json
import time
from threading import Semaphore, Thread

# Change this variable to edit total number of executions
TOTAL_EXECUTIONS = 1000

# Creates scan request 
def execute_shell_script(user, semaphore_dict, execution_count):

    print(f"Executing with user {user['user_id']} - Execution: {execution_count}")
    
    print(f"Executing with user {user['user_id']} - Execution: {execution_count}")

    # Use the user to run the pipeline scan on verademo-dotnet
    command = ["java", "-jar", "pipeline-scan.jar", "-vid", user["api_id"], "-vkey", user["api_secret"], "-f", "Verademo-dotnet.zip", "-jf", f"resultExec{execution_count}.json"]

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
            # TODO: Make sure this is necessary, probably don't need the user.get part.
            if user.get("executions", 0) < 5 and semaphore_dict[user["user_id"]].acquire(blocking=False):
                thread = Thread(target=execute_shell_script, args=(user, semaphore_dict, execution_count))
                thread.start()

                execution_count += 1

        time.sleep(1)

def main():
    # TODO: Remove unnecessary control_thread, replace with straight call to control_execution.

    # Load in data from json file
    with open("UsersAPIs1.json", "r") as file:
        data = json.load(file)
        users = data["users"]

    total_executions = TOTAL_EXECUTIONS

    # declares each user to get max 5 threads.
    semaphore_dict = {user["user_id"]: Semaphore(5) for user in users}
    
    # creates a thread that will run the 'control_execution' function with provided args as parameters.
    control_thread = Thread(target=control_execution, args=(users, semaphore_dict, total_executions))

    # Runs the thread to start 'control_execution'
    control_thread.start()
    
    # Wait until started thread terminates
    control_thread.join()

if __name__ == "__main__":
    main()