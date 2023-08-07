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
        dns_dict = dict()
        http_dict = dict()
        smb_dict = dict()

        for preset in presets:
            if preset['label'] == "All data":
                id = preset['id']

        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/presets/{id}/visualisations/dashboard-security/dns/list",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        dns = r_get.json()

        for d in dns:
            r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/presets/{id}/visualisations/dashboard-security/dns/components?property-value={d['label']}", headers=headers,verify=False)
            r_get.raise_for_status() #if there are any request errors

            details = r_get.json()
            dns_dict[d['label']] = details

        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/presets/{id}/visualisations/dashboard-security/http/list",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        http = r_get.json()

        for h in http:
            r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/presets/{id}/visualisations/dashboard-security/http/components?property-value={h['label']}", headers=headers,verify=False)
            r_get.raise_for_status() #if there are any request errors

            details = r_get.json()
            http_dict[h['label']] = details

        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/presets/{id}/visualisations/dashboard-security/smb/list",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        smb = r_get.json()

        for s in smb:
            r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/presets/{id}/visualisations/dashboard-security/smb/components?property-value={s['label']}", headers=headers,verify=False)
            r_get.raise_for_status() #if there are any request errors

            details = r_get.json()
            smb_dict[s['label']] = details

        return [dns_dict, http_dict, smb_dict]

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
sheet1.write(0, 2, 'Component')
sheet1.write(0, 3, 'IP')
sheet1.write(0, 4, 'MAC')

index = 1
for dns in data[0].keys():
    for component in data[0][dns]:
        sheet1.write(index, 0, dns)
        sheet1.write(index, 1, component['requestsCount'])
        sheet1.write(index, 2, component['label'])
        sheet1.write(index, 3, component['ip'])
        sheet1.write(index, 4, component['mac'])
        index += 1

sheet2 = workbook.add_worksheet("HTTP")

sheet2.write(0, 0, 'HTTP')
sheet2.write(0, 1, 'Request Count')
sheet2.write(0, 2, 'Component')
sheet2.write(0, 3, 'IP')
sheet2.write(0, 4, 'MAC')

index = 1
for http in data[1].keys():
    for component in data[1][http]:
        sheet2.write(index, 0, http)
        sheet2.write(index, 1, component['requestsCount'])
        sheet2.write(index, 2, component['label'])
        sheet2.write(index, 3, component['ip'])
        sheet2.write(index, 4, component['mac'])
        index += 1

sheet3 = workbook.add_worksheet("SMB")

sheet3.write(0, 0, 'SMB')
sheet3.write(0, 1, 'Request Count')
sheet3.write(0, 2, 'Component')
sheet3.write(0, 3, 'IP')
sheet3.write(0, 4, 'MAC')

index = 1
for smb in data[2].keys():
    for component in data[2][smb]:
        sheet3.write(index, 0, smb)
        sheet3.write(index, 1, component['requestsCount'])
        sheet3.write(index, 2, component['label'])
        sheet3.write(index, 3, component['ip'])
        sheet3.write(index, 4, component['mac'])
        index += 1

workbook.close()

print("Security Insight Report in this directory: " + str(Path.cwd()))

time.sleep(5)