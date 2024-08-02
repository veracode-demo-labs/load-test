import argparse
import os
import sys
import requests
import json
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_signing.credentials import get_credentials
from . import errors

def user_cleanup(id, key, api_base, headers):
    with open("outputs/UsersAPIs.json", "r") as file:
        data = json.load(file)
        users = data["users"]
    
    for user in users:
        response = requests.delete(api_base + f"api/authn/v2/users/{user["user_id"]}", auth=RequestsAuthPluginVeracodeHMAC(id, key), headers=headers)
        if response.ok:
            print(f"User with ID {user["user_id"]} successfuly deleted")
        elif response.status_code == 403:
            print(errors.PERMISSIONS_ERROR)
        
def team_cleanup(id, key, api_base, headers):
    with open("outputs/TeamAPI.json", "r") as file:
        data = json.load(file)
        teamID = data["team_id"]
    response = requests.delete(api_base + f"api/authn/v2/teams/{teamID}", auth=RequestsAuthPluginVeracodeHMAC(id, key), headers=headers)
    if response.ok:
        print(f"Team with ID {teamID} successfuly deleted")
    elif response.status_code == 403:
        print(errors.PERMISSIONS_ERROR)

def files_cleanup():
    os.remove("./outputs/TeamAPI.json")
    os.remove("./outputs/UsersAPIs.json")