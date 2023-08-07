import requests
import csv
from datetime import datetime
from pathlib import Path
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

center_token = input("Enter your Cyber Vision API Token: ")
center_ip = input("Enter the IP address of your Cyber Vision Center: ")

center_port = 443
center_base_url = "api/3.0"

def get_devices():
    try:
        headers = { "x-token-id": center_token }
        r_get = requests.get(f"https://{center_ip}:{center_port}/{center_base_url}/devices",headers=headers,verify=False)
        r_get.raise_for_status() #if there are any request errors

        #raw JSON data response
        raw_json_data = r_get.json()

        return raw_json_data

    except Exception as e:
        return f"Error when connecting: {e}"

def build_device_row(row,d):
    try:
        row['Hardware Name'] = d['label']
        if len(d['ip']) == 1:
            row['Internal IP Address'] = d['ip'][0]
        else:
            row['Internal IP Address'] = d['ip']
        row['External IP Address'] = ""
        row['Function'] = d['deviceType']
        os = []
        host = ""
        vendor = ""
        serial = ""
        models = []
        for component in d['components']:
            if component['normalizedProperties']:
                for property in component['normalizedProperties']:
                    if property['key'] == 'os-name':
                        os.append(property['value'])
                    elif property['key'] == 'model-ref':
                        models.append(property['value'])
                    elif property['key'] == 'serial-number':
                        serial = property['value']
            if component['otherProperties']:
                for prop in component['otherProperties']:
                    if prop['key'] == 'http-host':
                        host = prop['value']
                    elif prop['key'] == 'vendor':
                        vendor = prop['value']
        if len(os) == 0:
            row['Operating System'] = ""
        elif len(os) == 1:
            row['Operating System'] = os[0]
        else:
            row['Operating System'] = os
        row['Installed Software'] = ""
        row['Authorization Package'] = ""
        row['Category'] = d['components'][0]['group']['label']
        row['Default Gateway'] = ""
        row['Domain Name'] = ""
        row['FQDN'] = ""
        row['Host Name'] = host
        if len(d['mac']) == 1:
            row['MAC Address'] = d['mac'][0]
        else:
            row['MAC Address'] = d['mac']
        row['Manufacturer'] = vendor
        if len(models) == 0:
            row['Model'] = ""
        elif len(models) == 1:
            row['Model'] = models[0]
        else:
            row['Model'] = models
        row['Network Name Office'] = ""
        row['Primary DNS Server'] = ""
        row['Serial Number'] = serial
        row['Subnet Mask'] = ""
    except Exception as e: print(e)

def write_devices(filename,csv_delimiter,devices):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Hardware Name', 'Internal IP Address', 'External IP Address', 'Function', 'Operating System', 'Installed Software', 'Authorization Package', 'Category', 'Default Gateway', 'Domain Name', 'FQDN', 'Host Name', 'MAC Address', 'Manufacturer', 'Model', 'Network Name Office', 'Primary DNS Server', 'Serial Number', 'Subnet Mask']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=csv_delimiter)
        writer.writeheader()
        for d in devices:
            row = {}
            build_device_row(row,d)
            writer.writerow(row)
        print(f"LOG: Exported {len(devices)} into '{filename}'")

all_devices = get_devices()

now = datetime.now()

current_time = now.strftime("%m-%d-%Y_%H-%M-%S")

file_name = "Cyber Vision MCCAST Device Inventory_" + current_time + ".csv"

write_devices(file_name, ",", all_devices)

print("MCCAST Device Inventory Report in this directory: " + str(Path.cwd()))

time.sleep(5)