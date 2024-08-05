import argparse
import sys
import requests
import json
from modules import EnvSetup
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

# below is for Veracode US Commercial region. For logins in other region uncomment one of the other lines
API_BASE = "https://api.veracode.com/"
#API_BASE = "https://api.veracode.eu/" # for logins in the Veracode European Region
#API_BASE = "https://api.veracode.us/" # for logins in the Veracode US Federal Region
headers = {"User-Agent": "Python HMAC"}


def GenerateBaseLineFile(id, key, app_name, baseline_file):
    app_guid = GetApplicationGUID(id, key, app_name)
    flawsData = GetApplicationMitigatedFlaws(id, key, app_guid)
    CompareFlaws(flawsData, baseline_file)

def GetApplicationGUID(id, key, app_name):
    app_guid = ""
    response = requests.get(API_BASE + "appsec/v1/applications/?name=" + app_name, auth=RequestsAuthPluginVeracodeHMAC(id, key), headers=headers)
    
    if response.status_code == 200:
        print("Application GUID OK.")
        data = response.json()

        try:
            app_guid = data["_embedded"]["applications"][0]["guid"]
            print("Application found GUID = " + app_guid)
        except:
            print(f"Application Name not found.")
            exit(1)
    else:
        print("API Error.")
    return app_guid

# Uses the supplied guid to get flaw data.
def GetApplicationMitigatedFlaws(id, key, app_guid):
    flawsData = ""
    response = requests.get(API_BASE + "appsec/v2/applications/" + app_guid + "/findings?scan_type=STATIC", auth=RequestsAuthPluginVeracodeHMAC(id, key), headers=headers)
    
    if response.status_code == 200:
        print("Application Flaws OK.")
        flawsData = response.json()
        
    else:
        print("API Error.")
    
    return flawsData

def CompareFlaws(flaws_data, baseline_file):

    print("Comparing flaws...")
    
    approved_findings = []
    mitigated_flaws = []

    with open(baseline_file, 'r') as f1:
        base_data = json.load(f1)

    # Loop through findings from flaws
    for finding in flaws_data['_embedded']['findings']:
        if finding.get('finding_status', {}).get('resolution_status') == "APPROVED":
            approved_findings.append(finding)
    # Loop through approved findings, compare to baseline data
    # - if finding is recognized, add it to list of mitigated
    # - otherwise, not
    for finding in approved_findings:
        approved_file_name = finding.get('finding_details', {}).get('file_name')
        approved_line_number = finding.get('finding_details', {}).get('file_line_number')
        approved_qualified_function_name = finding.get('finding_details', {}).get('procedure')
        approved_attack_vector = finding.get('finding_details', {}).get('attack_vector')

        for base_finding in base_data['findings']:
            base_file_name = base_finding.get('files', {}).get('source_file', {}).get('file')
            base_line_number = base_finding.get('files', {}).get('source_file', {}).get('line')
            base_qualified_function_name = base_finding.get('files', {}).get('source_file', {}).get('qualified_function_name')
            base_attack_vector = base_finding.get('title')

            if approved_file_name in base_file_name and approved_line_number == base_line_number and approved_qualified_function_name == base_qualified_function_name and approved_attack_vector == base_attack_vector:
                mitigated_flaws.append(base_finding)

    base_data['findings'] = mitigated_flaws

    # Write mitigated flaws out to file.
    with open('outputs/Baseline_Mitigated_Result.json', 'w') as output_file:
        json.dump(base_data, output_file, indent=4)
    
    print("Example complete! Check the outputs/Baseline_Mitigated_Result.json file")

# Main part of code. Specifies command line arguments to be used in when the program runs

def main():
    parser = argparse.ArgumentParser()

    # Add command line arguments
    parser.add_argument('-id', '--id', '-ID', '--ID', required=False, help='Veracode API ID')
    parser.add_argument('-key', '--key', required=False, help='Veracode API Key')
    parser.add_argument('-profile', '--profile', required=False, help='Profile to pick from veracode credentials file. Default: default')
    parser.add_argument('-app', '--application', dest='app_name', required=True, help='Application Name in Veracode Platform')
    parser.add_argument('-baseline', '--baseline-file', dest='baseline_file', required=True, help='Baseline File to compare to (one of the resultExec files)')

    args = parser.parse_args()

    id = args.id
    key = args.key
    app_name = args.app_name
    baseline_file = args.baseline_file

    # Set up ID and key using credentials file or input flags
    id, key = EnvSetup.envSetup(args.id, args.key, args.profile)

    GenerateBaseLineFile(id, key, app_name, baseline_file)

if __name__ == "__main__":
    main()