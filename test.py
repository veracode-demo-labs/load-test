import json
import sys
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

# below is for Veracode US Commercial region. For logins in other region uncomment one of the other lines
api_base = "https://api.veracode.com/"
#api_base = "https://api.veracode.eu/" # for logins in the Veracode European Region
#api_base = "https://api.veracode.us/" # for logins in the Veracode US Federal Region

headers = {"User-Agent": "Python HMAC"}

users_json = {
    "users": []
}
users = []


if __name__ == "__main__":

    
    with open("CreateTeamInput.json", 'r') as f2:
        team_input = json.load(f2)

    try:
        print('creating team')
        response = requests.get("https://api.veracode.com/api/authn/v2/teams",
                                  auth=RequestsAuthPluginVeracodeHMAC(),
                                    headers=headers,
                                    #json=team_input,
                                    )
        if response.ok:
            data = response.json()
            for team in data["_embedded"]["teams"]:
                print(team["team_name"],": ",team['team_id'])
    except requests.RequestException as e:
        print("Whoops!")
        print(e)
        sys.exit(1)

    qtd_users = 2
    
    count_user = 0
    
    # Creates framework user data needed for obtaining creds
    with open("CreateUserInput.json", 'r') as f1:
        create_user_input = json.load(f1)

    create_user_input["user_name"] = "API_Itau_LoadTest_" + str(count_user)
    create_user_input["email_address"] = "rafaelmaiadeamorim+ILT" + str(count_user) + "@gmail.com"
    response = requests.post(api_base + "api/authn/v2/users", auth=RequestsAuthPluginVeracodeHMAC(), headers=headers, json=create_user_input)
    print(response)
    # Gets credentials for input number of users.
    # for _ in range(int(qtd_users)):
    #     userAPI = {
    #         "user_id": "",
    #         "api_id": "",
    #         "api_secret": ""
    #     }
    #     count_user += 1
    #     create_user_input["user_name"] = "API_Itau_LoadTest_" + str(count_user)
    #     create_user_input["email_address"] = "rafaelmaiadeamorim+ILT" + str(count_user) + "@gmail.com"
    #     print("User created: " + str(count_user))

    #     # Creates an API request using the python veracode-api-signing library to create a user
    #     response = requests.post(api_base + "api/authn/v2/users", auth=RequestsAuthPluginVeracodeHMAC(), headers=headers, json=create_user_input)
    #     print(response)
    #     # If successful auth, store api credentials from the response
    #     if response.ok:
    #         data = response.json()

    #         # Creating user tokens
    #         api_id, api_secret = CreateUsersIDKEY(data["user_id"])

    #         userAPI["user_id"] = data["user_id"]
    #         userAPI["api_id"] = api_id
    #         userAPI["api_secret"] = api_secret

    #         users_json["users"].append(userAPI)
    #     else:
    #         print("CreateUsers API Error.")
    
    # users_json["users"].append(userAPI)

    # # Write the output keys obtained to a new file
    # with open('UsersAPIs1.json', 'w') as output_file:
    #     json.dump(users_json, output_file, indent=4)



        