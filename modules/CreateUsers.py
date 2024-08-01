import argparse
import os
import sys
import requests
import json
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_signing.credentials import get_credentials

from dotenv import load_dotenv

# load environment variables in .env file
# load_dotenv()

# below is for Veracode US Commercial region. For logins in other region uncomment one of the other lines
API_BASE = "https://api.veracode.com/"
#API_BASE = "https://api.veracode.eu/" # for logins in the Veracode European Region
#API_BASE = "https://api.veracode.us/" # for logins in the Veracode US Federal Region
TEAM_NAME = 'load_test6'
headers = {"User-Agent": "Python HMAC"}

#TODO
def CreateTeam(id, key):
    with open("CreateTeamInput.json", 'r') as team_file:
        create_team_input = {
            "team_name": TEAM_NAME
        }
        print(create_team_input)
        print(get_credentials())
    response = requests.post(API_BASE + "api/authn/v2/teams", auth=RequestsAuthPluginVeracodeHMAC(id, key), headers=headers, json=create_team_input)
    print(response)
    if response.ok:
        print(response.json())
        team_id = response.json()['team_id']
        print(team_id)
        return
    elif response.status_code == 400:
        print("Invalid request: Check that TEAM_NAME does not already exist.")
        print("If it does, either delete the team with that name or change TEAM_NAME at the top of the modules/CreateUsers.py file")
    else:
        print(response.text)
    exit(1)

# Builds users based on the specified # of qtd_, getting 
def CreateUsersAPI(id, key, qtd_users, base_name, team_id):
    count_user = 0
    users_json = {
        "users": []
    }
    
    # Creates framework user data needed for obtaining creds
    with open("CreateUserInput.json", 'r') as f1:
        create_user_input = json.load(f1)

    # Gets credentials for input number of users.
    for _ in range(int(qtd_users)):
        userAPI = {
            "user_id": "",
            "api_id": "",
            "api_secret": ""
        }
        count_user += 1
        create_user_input["team_id"] = team_id 
        create_user_input["user_name"] = "API_LoadTest_" + base_name + "_" + str(count_user)
        create_user_input["email_address"] =  base_name + "+ILT_" + str(count_user) + "@gmail.com"
        print("User created: " + str(count_user))

        # Creates an API request using the python veracode-api-signing library to create a user
        response = requests.post(API_BASE + "api/authn/v2/users", auth=RequestsAuthPluginVeracodeHMAC(id, key), headers=headers, json=create_user_input)
        print(response)
        # If successful auth, store api credentials from the response
        if response.ok:
            data = response.json()

            # Creating user tokens
            api_id, api_secret = CreateUsersIDKEY(data["user_id"], id, key)

            userAPI["user_id"] = data["user_id"]
            userAPI["api_id"] = api_id
            userAPI["api_secret"] = api_secret

            users_json["users"].append(userAPI)
        else:
            print("CreateUsers API Error.")

    # Write the output keys obtained to a new file
    with open('UsersAPIs1.json', 'w') as output_file:
        json.dump(users_json, output_file, indent=4)

# Gets the api id and secret key of the specified user id.
def CreateUsersIDKEY(user_id, id, key):

    # Creates request to api_credentials to get creds
    response = requests.post(API_BASE + "api/authn/v2/api_credentials/user_id/" + user_id, auth=RequestsAuthPluginVeracodeHMAC(id, key), headers=headers)
    if response.status_code == 200:
        data = response.json()
        api_id = data["api_id"]
        api_secret = data["api_secret"]
        return api_id, api_secret
    else:
        print("CreateIDKEYAPI Error.")

# Main part of code. Specifies command line arguments to be used in when the program runs
# TODO: good idea to put this in a function, as opposed to being loose in file.
def runCreateUsers():
    parser = argparse.ArgumentParser()

    parser.add_argument('-ID', '--id', '-id', '--ID', required=False, help='Veracode API ID for creating users')
    parser.add_argument('-key', '--key', required=False, help='Veracode API Key for creating users')
    parser.add_argument('-profile', '--profile', required=False, help='Profile to pick from veracode credentials file. Default: default')
    parser.add_argument('-qtd_users', '--qtd_users', dest='qtd_users', required=False, help='The number of users to creates')
    parser.add_argument('-base_name', '--base_name', dest='base_name', required=False, help='A unique base username to generate users from')

    args = parser.parse_args()

    load_dotenv()

    # id = args.id
    # key = args.key
    id = os.getenv('veracode_api_key_id', args.id)
    key = os.getenv('veracode_api_key_secret', args.key)
    qtd_users = args.qtd_users # Number of users to make
    base_name = args.base_name

    if not all([id, key, qtd_users, base_name]):
        parser.print_usage()
        sys.exit(1)

    CreateUsersAPI(id, key, qtd_users, base_name)


