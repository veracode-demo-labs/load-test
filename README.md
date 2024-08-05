# Load Runner for Veracode Scanner

Original script by Rafael Maia de Amorim

## About
This script contains two executable python files:
- main.py
- Example.py

Also utilized is the `CreateUserInput.json` file, which is used by `CreateUsers`.

## Getting Started
Assuming you have python, download requirements by running `pip install -r requirements.txt`
    
For a simple load test, run `python main.py -base_name [unique base name]`. Note that the number of scans should be less than six times the number of users due to individual users being limited in the number of scans per second. This program will by default create 200 users and run 1000 scans. Please see the `main.py` section below for a full list of flags to customize your request. If you're using a login for a different region of Veracode, change to the correct region at the top of the main.py file

The Example.py file compares a scan results file with the approved mitigations in one of the applications present in the account associated with your API credentials. In order to use this, run `python Example.py -app [name of app] -baseline [scan results file]`.
    
For both of the above, API credentials are taken from the default profile in your `~/.veracode/credentials` file unless an ID and key, or different profile, are specified in the flags. Additional customization options are available through different flags.

## Files

### main.py

This python file executes the load-test by creating a team, filling it with users, and executing a number of scans using those users.

In order to use this, you must have a valid Veracode Platform account with enough permissions using the API HMAC.

```
    usage: main.py [-h] [-id ID] [-key KEY] [-profile PROFILE] [-qtd_users QTD_USERS] [-num_scans NUM_SCANS] [-team_name TEAM_NAME] [-skip_create] [-skip_usercleanup] [-app_name APP_NAME] -base_name BASE_NAME

    options:
    -h, --help            show this help message and exit
    -id ID, --id ID, -ID ID, --ID ID
                            Veracode API ID
    -key KEY, --key KEY   Veracode API Key
    -profile PROFILE, --profile PROFILE
                            Profile to pick from veracode credentials file. Default: default
    -qtd_users QTD_USERS, --qtd_users QTD_USERS
                            The number of users to creates
    -num_scans NUM_SCANS, --num_scans NUM_SCANS
                            The number of times the scan should be run
    -team_name TEAM_NAME, --team_name TEAM_NAME
                            A unique team name to store users
    -skip_create, --skip_create
                            Skip creating a team and users. You must already have a valid
                            outputs/UsersAPIs.json file
    -skip_usercleanup, --skip_usercleanup
                            Skip cleaning up teams and users after finished running.
    -app_name APP_NAME, --app_name APP_NAME
                            The full name of the app file in the resources folder to be scanned. Default:
                            Verademo-dotnet.zip
    -base_name BASE_NAME, --base_name BASE_NAME
                            A unique base username to generate users from
```

### Example.py
```
    usage: Example.py [-h] [-id ID] [-key KEY] [-profile PROFILE] -app APP_NAME -baseline BASELINE_FILE

    options:
    -h, --help            show this help message and exit
    -id ID, --id ID, -ID ID, --ID ID
                            Veracode API ID
    -key KEY, --key KEY   Veracode API Key
    -profile PROFILE, --profile PROFILE
                            Profile to pick from veracode credentials file. Default: default
    -app APP_NAME, --application APP_NAME
                            Application Name in Veracode Platform
    -baseline BASELINE_FILE, --baseline-file BASELINE_FILE
                            Baseline File to compare to (one of the resultExec files)
```
