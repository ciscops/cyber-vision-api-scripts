import requests
import xlsxwriter
from datetime import datetime
from pathlib import Path
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

center_token = input("Enter your Cyber Vision API Token: ")
center_ip = input("Enter the IP address of your Cyber Vision Center: ")

center_port = 443
center_base_url = "api/3.0"

def get_component():
    try:
        headers = { "x-token-id": center_token }
        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/components",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        #raw JSON data response
        devices = r_get.json()

        variables = dict()
        credentials = dict()

        for device in devices:
            if device['variablesCount'] > 0:
                id = device['id']
                v_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/components/{id}/variables",headers=headers,verify=False)
                v_get.raise_for_status() #if there are any request errors

                vars = v_get.json()
                variables[device['label']] = vars
            
            if device['credentialsCount'] > 0:
                id = device['id']
                c_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/components/{id}/credentials",headers=headers,verify=False)
                c_get.raise_for_status() #if there are any request errors

                creds = c_get.json()
                credentials[device['label']] = creds

        return [variables, credentials]

    except Exception as e:
        return f"Error when connecting: {e}"

def get_device():
    try:
        headers = { "x-token-id": center_token }
        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/devices",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        #raw JSON data response
        devices = r_get.json()

        variables = dict()
        credentials = dict()

        for device in devices:
            if device['variablesCount'] > 0:
                id = device['id']
                v_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/devices/{id}/variables",headers=headers,verify=False)
                v_get.raise_for_status() #if there are any request errors

                vars = v_get.json()
                variables[device['label']] = vars
            
            if device['credentialsCount'] > 0:
                id = device['id']
                c_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/devices/{id}/credentials",headers=headers,verify=False)
                c_get.raise_for_status() #if there are any request errors

                creds = c_get.json()
                credentials[device['label']] = creds

        # Note: maybe look for IP address of accessed by devices/components instead of label

        return [variables, credentials]

    except Exception as e:
        return f"Error when connecting: {e}"

device_data = get_device()
component_data = get_component()

now = datetime.now()

current_time = now.strftime("%m-%d-%Y_%H-%M-%S")

file_name = "Cyber Vision Variables and Credentials_" + current_time + ".xlsx"

workbook = xlsxwriter.Workbook(file_name)
sheet1 = workbook.add_worksheet("Variables")

sheet1.write(0, 0, 'Device')
sheet1.write(0, 1, 'Variable')
sheet1.write(0, 2, 'Protocol')
sheet1.write(0, 3, 'Details')
sheet1.write(0, 4, 'Types')
sheet1.write(0, 5, 'Accessed By')
sheet1.write(0, 6, 'First Access')
sheet1.write(0, 7, 'Last Access')

index = 1
lastIndex = 0
for device in device_data[0].keys():
    for var in device_data[0][device]:
        sheet1.write(index, 0, device)
        sheet1.write(index, 1, var['label'])
        sheet1.write(index, 2, var['protocol'])
        sheet1.write(index, 3, var['category'])

        types = ""
        for type in var['types']:
            types += type + ", "
        types = types[0:len(types)-2]

        sheet1.write(index, 4, types)

        accesses = ""
        for access in var['accesses']:
            if 'device' in access:
                accesses += access['device']['label'] + ", "
            else:
                accesses += access['component']['label'] + ", "
        accesses = accesses[0:len(accesses)-2]
        
        sheet1.write(index, 5, accesses)
        sheet1.write(index, 6, datetime.fromtimestamp(int(var['firstAccess'])//1000).strftime("%m-%d-%Y, %H:%M:%S"))
        sheet1.write(index, 7, datetime.fromtimestamp(int(var['lastAccess'])//1000).strftime("%m-%d-%Y, %H:%M:%S"))
        index += 1
        lastIndex = index

lastIndex += 2

sheet1.write(lastIndex, 0, 'Component')
sheet1.write(lastIndex, 1, 'Variable')
sheet1.write(lastIndex, 2, 'Protocol')
sheet1.write(lastIndex, 3, 'Details')
sheet1.write(lastIndex, 4, 'Types')
sheet1.write(lastIndex, 5, 'Accessed By')
sheet1.write(lastIndex, 6, 'First Access')
sheet1.write(lastIndex, 7, 'Last Access')

index = lastIndex + 1
for component in component_data[0].keys():
    for var in component_data[0][component]:
        sheet1.write(index, 0, component)
        sheet1.write(index, 1, var['label'])
        sheet1.write(index, 2, var['protocol'])
        sheet1.write(index, 3, var['category'])

        types = ""
        for type in var['types']:
            types += type + ", "
        types = types[0:len(types)-2]

        sheet1.write(index, 4, types)

        accesses = ""
        for access in var['accesses']:
            if 'device' in access:
                accesses += access['device']['label'] + ", "
            else:
                accesses += access['component']['label'] + ", "
        accesses = accesses[0:len(accesses)-2]
        
        sheet1.write(index, 5, accesses)
        sheet1.write(index, 6, datetime.fromtimestamp(int(var['firstAccess'])//1000).strftime("%m-%d-%Y, %H:%M:%S"))
        sheet1.write(index, 7, datetime.fromtimestamp(int(var['lastAccess'])//1000).strftime("%m-%d-%Y, %H:%M:%S"))
        index += 1
        lastIndex = index

sheet2 = workbook.add_worksheet("Credentials")

sheet2.write(0, 0, 'Device')
sheet2.write(0, 1, 'Username')
sheet2.write(0, 2, 'Password')

index = 1
lastIndex = 0
for device in device_data[1]:
    for cred in device_data[1][device]:
        sheet2.write(index, 0, device)
        sheet2.write(index, 1, cred['username'])
        sheet2.write(index, 2, cred['password'])
        index += 1
        lastIndex = index

lastIndex += 2

sheet2.write(lastIndex, 0, 'Component')
sheet2.write(lastIndex, 1, 'Username')
sheet2.write(lastIndex, 2, 'Password')

index = lastIndex + 1
for component in component_data[1]:
    for cred in component_data[1][component]:
        sheet2.write(index, 0, component)
        sheet2.write(index, 1, cred['username'])
        sheet2.write(index, 2, cred['password'])
        index += 1
        lastIndex = index

workbook.close()

print("Variables and Credentials Report in this directory: " + str(Path.cwd()))

time.sleep(5)