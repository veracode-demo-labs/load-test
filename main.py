import argparse
from modules import EnvSetup, CreateUsers

parser = argparse.ArgumentParser()

parser.add_argument('-ID', '--id', '-id', '--ID', required=False, help='Veracode API ID for creating users')
parser.add_argument('-key', '--key', required=False, help='Veracode API Key for creating users')
parser.add_argument('-profile', '--profile', required=False, help='Profile to pick from veracode credentials file. Default: default')
parser.add_argument('-qtd_users', '--qtd_users', dest='qtd_users', required=True, help='The number of users to creates',)
parser.add_argument('-base_name', '--base_name', dest='base_name', required=True, help='A unique base username to generate users from')

args = parser.parse_args()

# id = args.id
# key = args.key
qtd_users = args.qtd_users # Number of users to make
base_name = args.base_name

# Get Env vars
id, key = EnvSetup.envSetup(args.id, args.key, args.profile)
print(id, key)

CreateUsers.CreateUsersAPI(id, key, qtd_users, base_name, None)


# print(createUsers(id, key))
# print(result)
# RunTests()

