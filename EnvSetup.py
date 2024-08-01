# Fetch Credentials

import veracode_api_signing.credentials as vcreds

"""
Setup environment variables ID, Key
"""
def envSetup(id=None, key=None, profile=None, auth_file=None):

    api_key_id = id
    api_key_secret = key
    vcreds.PROFILE_DEFAULT=profile if profile else None

    if not (id or key):
        api_key_id, api_key_secret = vcreds.get_credentials(auth_file)
    
    return api_key_id, api_key_secret