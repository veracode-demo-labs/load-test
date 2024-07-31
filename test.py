import json
import sys
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

# below is for Veracode US Commercial region. For logins in other region uncomment one of the other lines
api_base = "https://api.veracode.com/appsec/v1"
#api_base = "https://api.veracode.eu/appsec/v1" # for logins in the Veracode European Region
#api_base = "https://api.veracode.us/appsec/v1" # for logins in the Veracode US Federal Region

headers = {"User-Agent": "Python HMAC"}


if __name__ == "__main__":

    try:
        response = requests.get(api_base + "/applications", auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
    except requests.RequestException as e:
        print("Whoops!")
        print(e)
        sys.exit(1)

    if response.ok:
        data = response.json()
        for app in data["_embedded"]["applications"]:
            print(app["profile"]["name"])
    else:
        print(response.status_code)
    with open("CreateUserInput.json", 'r') as f1:
        create_user_input = json.load(f1)

    userAPI = {
        "user_id": "",
        "api_id": "",
        "api_secret": ""
    }
        
    create_user_input["user_name"] = "API_Itau_LoadTest_"
    create_user_input["email_address"] = "rafaelmaiadeamorim+ILT@gmail.com"
    print("User created: ")
    print(create_user_input)
    try:
        response = requests.post("https://api.veracode.com/api/authn/v2/users",
                                  auth=RequestsAuthPluginVeracodeHMAC(),
                                    headers=headers,
                                    json=create_user_input,
                                    )
        print(response)
    except requests.RequestException as e:
        print("Whoops!")
        print(e)
        sys.exit(1)

    if response.ok:
        print('success response')
        data = response.json()
    else:
        print(response.status_code)
        