import argparse
import os
import sys
import requests
import json
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_signing.credentials import get_credentials
from . import errors



def CreateTeam(id, key, team_name, api_base, headers):
    create_team_input = {
        "team_name": team_name
    }
    # Create a new team with the given team name
    response = requests.post(api_base + "api/authn/v2/teams", auth=RequestsAuthPluginVeracodeHMAC(id, key), headers=headers, json=create_team_input)
    if response.ok:
        # If successful, return the id of the newly created team
        team_id = response.json()['team_id']
        with open('./outputs/TeamAPI.json', 'w') as output_file:
            json.dump(response.json(), output_file, indent=4)
        return team_id
    elif response.status_code == 400:
        print("Invalid request: Check that a team name with TEAM_NAME does not already exist.\n"
              "The team name can be changed at the top of main.py or by setting the -team_name [TEAM NAME] flag")
    elif response.status_code == 403:
        print(errors.PERMISSIONS_ERROR)
    else:
        print(f"Error creating team: {response.text}")
    # Exit the program if we don't return from the success case
    exit(1)

# Builds users based on the specified # of qtd_, getting 
def CreateUsersAPI(id, key, qtd_users, base_name, team_id, api_base, headers):
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
        user_input_username = "API_LoadTest_" + base_name + "_" + str(count_user)
        create_user_input["user_name"] = user_input_username
        create_user_input["email_address"] =  base_name + "+ILT_" + str(count_user) + "@gmail.com"
        

        # Creates an API request using the python veracode-api-signing library to create a user
        response = requests.post(api_base + "api/authn/v2/users", auth=RequestsAuthPluginVeracodeHMAC(id, key), headers=headers, json=create_user_input)
        # If successful auth, store api credentials from the response
        if response.ok:
            data = response.json()

            # Creating user tokens
            api_id, api_secret = CreateUsersIDKEY(data["user_id"], id, key, api_base, headers)

            userAPI["user_id"] = data["user_id"]
            userAPI["api_id"] = api_id
            userAPI["api_secret"] = api_secret

            users_json["users"].append(userAPI)

            print("User created: " + user_input_username)
        elif response.status_code == 400:
            print(f"A Veracode user already exists with username {user_input_username}.\n"
                   "Skipping user... Try changing the -base_name flag!")
        elif response.status_code == 403:
            print(errors.PERMISSIONS_ERROR)
        else:
            print(f"Error creating users: {response.text}")

    # Write the output keys obtained to a new file
    with open('./outputs/UsersAPIs.json', 'w') as output_file:
        json.dump(users_json, output_file, indent=4)
    
# Gets the api id and secret key of the specified user id.
def CreateUsersIDKEY(user_id, id, key, api_base, headers):

    # Creates request to api_credentials to get creds
    response = requests.post(api_base + "api/authn/v2/api_credentials/user_id/" + user_id, auth=RequestsAuthPluginVeracodeHMAC(id, key), headers=headers)
    if response.status_code == 200:
        data = response.json()
        api_id = data["api_id"]
        api_secret = data["api_secret"]
        return api_id, api_secret
    else:
        print("CreateIDKEYAPI Error.")
