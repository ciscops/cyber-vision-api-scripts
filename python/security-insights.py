import requests
import xlsxwriter
from pathlib import Path
import time
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

center_token = input("Enter your Cyber Vision API Token: ")
center_ip = input("Enter the IP address of your Cyber Vision Center: ")

center_port = 443
center_base_url = "api/3.0"

def get():
    try:
        headers = { "x-token-id": center_token }
        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/presets",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        #raw JSON data response
        presets = r_get.json()

        id = 0

        for preset in presets:
            if preset['label'] == "All data":
                id = preset['id']

        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/presets/{id}/visualisations/dashboard-security/dns/list",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        dns = r_get.json()

        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/presets/{id}/visualisations/dashboard-security/http/list",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        http = r_get.json()

        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/presets/{id}/visualisations/dashboard-security/smb/list",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        smb = r_get.json()

        return [dns, http, smb]

    except Exception as e:
        return f"Error when connecting: {e}"

data = get()

now = datetime.now()

current_time = now.strftime("%m-%d-%Y_%H-%M-%S")

file_name = "Cyber Vision Security Insights_" + current_time + ".xlsx"

workbook = xlsxwriter.Workbook(file_name)
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

sheet2 = workbook.add_worksheet("HTTP")

sheet2.write(0, 0, 'HTTP')
sheet2.write(0, 1, 'Request Count')
sheet2.write(0, 2, 'Component Count')

index = 1
for http in data[1]:
    sheet2.write(index, 0, http['label'])
    sheet2.write(index, 1, http['value'])
    sheet2.write(index, 2, http['componentsCount'])
    index += 1

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

workbook.close()

print("Security Insight Report in this directory: " + str(Path.cwd()))

time.sleep(5)