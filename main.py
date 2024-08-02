import argparse
from modules import Cleanup, EnvSetup, CreateUsers, RunTests, Example

parser = argparse.ArgumentParser()

QTD_USERS = 200
NUM_SCANS = 1000
TEAM_NAME = "load_test"

# below is for Veracode US Commercial region. For logins in other region uncomment one of the other lines
API_BASE = "https://api.veracode.com/"
#API_BASE = "https://api.veracode.eu/" # for logins in the Veracode European Region
#API_BASE = "https://api.veracode.us/" # for logins in the Veracode US Federal Region
headers = {"User-Agent": "Python HMAC"}

# Add command line arguments
parser.add_argument('-id', '--id', '-ID', '--ID', required=False, help='Veracode API ID for creating users')
parser.add_argument('-key', '--key', required=False, help='Veracode API Key for creating users')
parser.add_argument('-profile', '--profile', required=False, help='Profile to pick from veracode credentials file. Default: default')
parser.add_argument('-qtd_users', '--qtd_users', dest='qtd_users', required=False, help='The number of users to creates',)
parser.add_argument('-num_scans', '--num_scans', dest='num_scans', required=False, help='The number of times the scan should be run',)
parser.add_argument('-team_name', '--team_name', dest='team_name', required=False, help='A unique team name to store users')
parser.add_argument('-skip_create', '--skip_create', dest='skip_create', action='store_true', required=False, help='Skip creating a team and users. You must already have a valid outputs/UsersAPIs.json file')
parser.add_argument('-skip_usercleanup', '--skip_usercleanup', dest='skip_usercleanup', action='store_true', required=False, help='Skip cleaning up teams and users after finished running.')
parser.add_argument('-base_name', '--base_name', dest='base_name', required=True, help='A unique base username to generate users from')

args = parser.parse_args()

print("Run 'python main.py -help' to get more information on settable flags")

# Set variables
base_name = args.base_name
qtd_users = args.qtd_users if args.qtd_users else QTD_USERS
num_scans = args.num_scans if args.num_scans else NUM_SCANS
team_name = args.team_name if args.team_name else TEAM_NAME

# Get Env vars
id, key = EnvSetup.envSetup(args.id, args.key, args.profile)

# Create team and users to run scans
if not args.skip_create:
    print("Creating Team and Users...")
    try:
        open('./outputs/UsersAPIs.json', 'x')
        open('./outputs/TeamAPI.json', 'x')
    except FileExistsError:
        print("outputs/UsersAPIs.json or outputs/TeamAPI.json already exists! Please move or rename the file(s).")
        exit(1)
    teamid = CreateUsers.CreateTeam(id, key, team_name, API_BASE, headers)
    CreateUsers.CreateUsersAPI(id, key, qtd_users, base_name, teamid, API_BASE, headers)
    print("Users successfully created!")

# Run scans using users
print("Running Scans...")
RunTests.run_tests(num_scans)

# Delete used team and users
if not args.skip_usercleanup:
    print("Cleaning Up...")
    Cleanup.user_cleanup(id, key, API_BASE, headers)
    Cleanup.team_cleanup(id, key, API_BASE, headers)
    Cleanup.files_cleanup()

exit(0)