import argparse
import os
import sys
import requests
import json
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from dotenv import load_dotenv

# load environment variables in .env file
# load_dotenv()

# below is for Veracode US Commercial region. For logins in other region uncomment one of the other lines
api_base = "https://api.veracode.com/"
#api_base = "https://api.veracode.eu/" # for logins in the Veracode European Region
#api_base = "https://api.veracode.us/" # for logins in the Veracode US Federal Region
headers = {"User-Agent": "Python HMAC"}

users_json = {
    "users": []
}
users = []


# Builds users based on the specified # of qtd_users, getting 
def CreateUsersAPI(id, key, qtd_users, file_name):
    count_user = 0
    
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
        create_user_input["user_name"] = "API_LoadTest_" + base_name + "_" + str(count_user)
        create_user_input["email_address"] =  base_name + "+ILT_" + str(count_user) + "@gmail.com"
        print("User created: " + str(count_user))

        # Creates an API request using the python veracode-api-signing library to create a user
        response = requests.post(api_base + "api/authn/v2/users", auth=RequestsAuthPluginVeracodeHMAC(id, key), headers=headers, json=create_user_input)
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
    response = requests.post(api_base + "api/authn/v2/api_credentials/user_id/" + user_id, auth=RequestsAuthPluginVeracodeHMAC(id, key), headers=headers)
    if response.status_code == 200:
        data = response.json()
        api_id = data["api_id"]
        api_secret = data["api_secret"]
        return api_id, api_secret
    else:
        print("CreateIDKEYAPI Error.")

# Main part of code. Specifies command line arguments to be used in when the program runs
# TODO: good idea to put this in a function, as opposed to being loose in file.
parser = argparse.ArgumentParser()

parser.add_argument('-ID', '--id', required=True, help='ID')
parser.add_argument('-key', '--key', required=True, help='Key')
parser.add_argument('-qtd_users', '--qtd_users', dest='qtd_users', required=True, help='Qtd Users')
parser.add_argument('-base_name', '--base_name', dest='base_name', required=True, help='Unique Base Username')

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
