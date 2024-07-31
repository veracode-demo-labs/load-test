# Load Runner for Veracode Scanner

## About
This script contains three python files:
- CreateUsers.py
- Example.py
- RunTests.py

These files are run in one script, `script.sh`, for automation. Also utilized is the `CreateUserInput.json` file, which is used by `CreateUsers`.

## Getting Started
    Assuming you have python, download requirements by running `pip install -r requirements.txt`
    
    Then you are ready to go.


## Files

### script.sh

This is a bash script that combines the usage of CreateUsers and RunTests. It should create users, and then use output file for RunTests.

### CreateUsers.py

This python file creates a specified number of users, fetches their account info in the format
```
    {
    "users": [
        {
            "user_id": "",
            "api_id": "",
            "api_secret": ""
        }
    ]
}
```
and then writes the info to a file, which is to be used in the RunTests.py script.

In order to use this, you must have a valid Veracode Platform account with the ability to create new users using the API HMAC.

```
    usage: CreateUsers.py [-h] -ID ID -key KEY -qtd_users QTD_USERS -file_name
                        FILE_NAME

    options:
    -h, --help            show this help message and exit
    -ID ID, --id ID       ID
    -key KEY, --key KEY   Key
    -qtd_users QTD_USERS, --qtd_users QTD_USERS
                            Qtd Users
    -file_name FILE_NAME, --file_name FILE_NAME
                            File
```

### RunTests.py

Reads user API data from a json file created with CreateUsers.py and uses users to run multi-threaded scans. With this script each user can have up to 5 scanners at once.

This points the static scanner at Verademo-dotnet.zip, the packaged version of Verademo-dotnet.

### Example.py
```
    usage: Example.py [-h] -ID ID -key KEY -app APP_NAME -baseline BASELINE_FILE

    options:
      -h, --help            show this help message and exit
      -ID ID, --id ID       ID
      -key KEY, --key KEY   Key
      -app APP_NAME, --application APP_NAME
                            Application Name
      -baseline BASELINE_FILE, --baseline-file BASELINE_FILE
                            Baseline File
```