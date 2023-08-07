import requests
import sys
import csv
import pandas as pd
from datetime import datetime
import urllib3
from pathlib import Path
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv'
r = requests.get(url, allow_redirects=True)
open('known_exploited_vulnerabilities.csv', 'wb').write(r.content)

args = sys.argv
filename = input("Please enter the filename of your Cyber Vision CEV report (with the .xlsx extension): ")

KEVs = []
kev_titles = []
kev_summaries = []
kev_vendors = []

with open("known_exploited_vulnerabilities.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            KEVs.append(row[0])
            kev_titles.append(row[3])
            kev_summaries.append(row[5])
            kev_vendors.append(row[1])
        line_count += 1

vul = pd.read_excel(filename, sheet_name="Vulnerabilities", usecols="Q")
vul_db = pd.read_excel(filename, sheet_name="Vulnerability Database")

vulnerabilities = vul["CVE"].tolist()
vul_titles = vul_db["Title"].tolist()
vul_summaries = vul_db["Summary"].tolist()
cv_known = vul_db["CVE"].tolist()

cv_report = []
kev_report = []

for i in range(0, len(vulnerabilities)):
    vuln = vulnerabilities[i]
    if vuln in cv_known:
        cv_report.append((vuln, vul_titles[i], vul_summaries[i]))
    if vuln in KEVs:
        kev_report.append((vuln, kev_titles[i], kev_summaries[i], kev_vendors[i]))

now = datetime.now()

current_time = now.strftime("%m-%d-%Y_%H-%M-%S")

file_name = "Cyber-Vision-KEV-Report_" + current_time + ".html"

filewriter = open(file_name,"w", encoding="utf-8")

opening = "<html>\n<head>\n<title> \nKEV Report \
           </title>\n<link rel='stylesheet' href='styles.css'>\n</head> <body><h1>KEVs Found in Your Network</h1>"

cv_string = "<h3>KEVs From CyberVision's Database</h3>\n"

if(len(cv_report) == 0):
    cv_string += "<p>No vulnerabilities found</p>"
else:
    cv_string += "<table>\n<tr>\n<th class='col1'>CVE Id</th>\n<th class='col2'>Title</th>\n<th class='col3'>Summary</th>\n</tr>"
    for vuln in cv_report:
        cv_string += "<tr>\n<td>" + str(vuln[0]) + "</td>\n<td>" + str(vuln[1]) + "</td>\n<td>" + str(vuln[2]) + "</td>\n</tr>\n"
    cv_string += "</table>"

cv_string += "<br>"

kev_string = "<h3>KEVs From CISA's Database</h3>\n"

if(len(kev_report) == 0):
    kev_string += "<p>No vulnerabilities found</p>"
else:
    kev_string += "<table>\n<tr>\n<th class='col4'>CVE Id</th>\n<th class='col5'>Title</th>\n<th class='col6'>Vendor</th>\n<th class='col7'>Summary</th>\n</tr>"
    for vuln in kev_report:
        kev_string += "<tr>\n<td>" + str(vuln[0]) + "</td>\n<td>" + str(vuln[1]) + "</td>\n<td>" + str(vuln[3]) + "</td>\n<td>" + str(vuln[2]) + "</td>\n</tr>\n"
    kev_string += "</table>"

kev_string += "<br>"

closing = "</body></html>"

html_content = opening + cv_string + kev_string + closing
   
filewriter.write(html_content)
              
filewriter.close()

print("KEV Report in this directory: " + str(Path.cwd()))

time.sleep(5)