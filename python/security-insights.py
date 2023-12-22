import requests
import xlsxwriter
from pathlib import Path
import time
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from requests import get

center_token = input("Enter your Cyber Vision API Token: ")
center_ip = input("Enter the IP address of your Cyber Vision Center: ")

center_port = 443
center_base_url = "api/3.0"

def get():
    try:
        headers = { "x-token-id": center_token }

        print("Fetching preset id data...")

        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/presets",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        #raw JSON data response
        presets = r_get.json()

        id = 0

        for preset in presets:
            if preset['label'] == "All data":
                id = preset['id']

        print("Fetching DNS data...")

        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/presets/{id}/visualisations/dashboard-security/dns/list",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        dns = r_get.json()

        print("" + str(len(dns)) + " DNS requests found")

        print("Fetching HTTP data...")

        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/presets/{id}/visualisations/dashboard-security/http/list",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        http = r_get.json()

        for request in http:
            loc = get(f'https://ipapi.co/{request["label"]}/json/')
            request["name"] = loc["org"]

        print("" + str(len(http)) + " HTTP requests found")

        print("Fetching SMB data...")

        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/presets/{id}/visualisations/dashboard-security/smb/list",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        smb = r_get.json()

        print("" + str(len(smb)) + " Server Message Block (SMB) Trees found")

        print("Checking Cyber Vision version...")

        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/version",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        version = r_get.json()

        external = {"devices": [], "components": []}

        if version["major"] == 4 and version["minor"] == 3:
            print("Version is at least 4.3.x")
            print("Fetching device ids...")

            r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/devices",headers=headers,verify=False)
            r_get.raise_for_status() #if there are any request errors

            devices = r_get.json()

            print("Fetching component ids...")

            r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/components",headers=headers,verify=False)
            r_get.raise_for_status() #if there are any request errors

            components = r_get.json()

            print("Fetching external communications for devices...")
            
            for device in devices:
                if device["externalCommunicationsCount"] > 0:
                    r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/devices/{device['id']}/externalCommunications",headers=headers,verify=False)
                    r_get.raise_for_status() #if there are any request errors

                    temp = r_get.json()

                    device_data = {'label': device['label'], 'timestamp': 0, 'count': 0, 'ip': temp[0]['sourceIP'], 'mac': device['mac'], 'volume': 0}

                    for activity in temp:
                        if activity['lastSeen'] > device_data['timestamp']:
                            device_data['timestamp'] = activity['lastSeen']
                        device_data['count'] += 1
                        device_data['volume'] += activity['sentByDevice']

                    external['devices'].append(device_data)

            print("Fetching external communications for components...")

            for component in components:               
                 if component["externalCommunicationsCount"] > 0:
                    r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/components/{component['id']}/externalCommunications",headers=headers,verify=False)
                    r_get.raise_for_status() #if there are any request errors

                    temp = r_get.json()

                    component_data = {'label': component['label'], 'timestamp': 0, 'count': 0, 'ip': temp[0]['sourceIP'], 'mac': component['mac'], 'volume': 0}

                    for activity in temp:
                        if activity['lastSeen'] > component_data['timestamp']:
                            component_data['timestamp'] = activity['lastSeen']
                        component_data['count'] += 1
                        component_data['volume'] += activity['sentByDevice']

                    external['components'].append(component_data)

        return [dns, http, smb, external]

    except Exception as e:
        return f"Error when connecting: {e}"

data = get()

print("Finished fetching API data")

now = datetime.now()

current_time = now.strftime("%m-%d-%Y_%H-%M-%S")

file_name = "Cyber Vision Security Insights_" + current_time + ".xlsx"

workbook = xlsxwriter.Workbook(file_name)

print("Writing DNS data to Excel")

sheet1 = workbook.add_worksheet("DNS")

sheet1.write(0, 0, 'DNS')
sheet1.write(0, 1, 'Request Count')
sheet1.write(0, 2, 'Component Count')

index = 1
for dns in data[0]:
    sheet1.write(index, 0, dns['label'])
    sheet1.write(index, 1, dns['value'])
    sheet1.write(index, 2, dns['componentsCount'])
    index += 1

print("Writing HTTP data to Excel")

sheet2 = workbook.add_worksheet("HTTP")

sheet2.write(0, 0, 'HTTP')
sheet2.write(0, 1, 'Request Count')
sheet2.write(0, 2, 'Component Count')
sheet2.write(0, 3, "Name")

index = 1
for http in data[1]:
    sheet2.write(index, 0, http['label'])
    sheet2.write(index, 1, http['value'])
    sheet2.write(index, 2, http['componentsCount'])
    sheet2.write(index, 3, http['name'])
    index += 1

print("Writing SMB data to Excel")

sheet3 = workbook.add_worksheet("SMB")

sheet3.write(0, 0, 'SMB')
sheet3.write(0, 1, 'Request Count')
sheet3.write(0, 2, 'Component Count')

index = 1
for smb in data[2]:
    sheet3.write(index, 0, smb['label'])
    sheet3.write(index, 1, smb['value'])
    sheet3.write(index, 2, smb['componentsCount'])
    index += 1

print("Writing External Communication data to Excel")
sheet4 = workbook.add_worksheet("External Communication")
index = 1

if len(data[3]["devices"]) > 0 or len(data[3]["components"]) > 0:

    if len(data[3]['devices']) > 0:
        sheet4.write(0, 0, 'Device')
        sheet4.write(0, 1, 'IP')
        sheet4.write(0, 2, 'MAC')
        sheet4.write(0, 3, 'Count')
        sheet4.write(0, 4, "Last Activity")
        sheet4.write(0, 5, "Data Volume")
        for device in data[3]['devices']:
            sheet4.write(index, 0, device['label'])
            sheet4.write(index, 1, device['ip'])
            sheet4.write(index, 2, device['mac'])
            sheet4.write(index, 3, device['count'])
            sheet4.write(index, 4, datetime.fromtimestamp(device['timestamp']//1000).strftime("%b %d, %Y %I:%M:%S %p"))
            sheet4.write(index, 5, device['volume'])
            index += 1
        index += 1
    else:
        index = 0

    if len(data[3]["components"]) > 0:
        sheet4.write(index, 0, 'Component')
        sheet4.write(index, 1, 'IP')
        sheet4.write(index, 2, 'MAC')
        sheet4.write(index, 3, 'Count')
        sheet4.write(index, 4, "Last Activity")
        sheet4.write(index, 5, "Data Volume")
        index += 1
        for component in data[3]["components"]:
            sheet4.write(index, 0, component['label'])
            sheet4.write(index, 1, component['ip'])
            sheet4.write(index, 2, component['mac'])
            sheet4.write(index, 3, component['count'])
            sheet4.write(index, 4, datetime.fromtimestamp(component['timestamp']//1000).strftime("%b %d, %Y %I:%M:%S %p")) 
            sheet4.write(index, 5, component['volume'])
            index += 1

workbook.close()

print("Security Insight Report in this directory: " + str(Path.cwd()))

time.sleep(5)