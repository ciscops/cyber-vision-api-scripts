from pathlib import Path
import time
from datetime import datetime
import os
import tarfile

directory = str(Path.cwd())
 
files = os.listdir(directory)
files = [f for f in files if os.path.isfile(directory +'/'+f) and '.tgz' in f and 'sbs-diag' in f]

if len(files) > 0:
    print(".tgz files detected")
    for index in range(len(files)):
        print(str(index+1) + ". " + files[index])
    response = int(input("Please input the number of the .tgz you want to unzip (0 to skip): ").strip().replace(" ", ""))

    if response > 0:
        file = tarfile.open(files[response-1])
        file.extractall()
        file.close()
            
folders = []

rootdir = str(Path.cwd())
for it in os.scandir(rootdir):
    if it.is_dir():
        folders.append(it.path)

diag_folders = []

for name in folders:
    if "sbs-diag" in name:
        diag_folders.append(name[name.rindex('\\')+1:len(name)])

if len(diag_folders) == 0:
    print("No Cyber Vision diag bundle detected in this directory.")
    folder = input("Please input the name of your diag folder: ")
    while not (folder in folders):
        print("Diag bundle " + folder + " not found in diag bundle..")
        folder = input("Please input the name of your diag folder: ")
elif len(diag_folders) > 1:
    print("Multiple diag bundles found.")
    for index in range(len(diag_folders)):
        print(str(index+1) + ". " + diag_folders[index])
    i = int(input("Please input the number of the diag folder you'd like to use: ").strip())
    folder = diag_folders[i-1]
else:
    print("Diag bundle " + diag_folders[0] + " found.")
    folder = diag_folders[0]

print("Generating diagnostic report...")


string = ""

if(os.path.isfile(directory + '\\' + folder + '\\' + 'date')):
    string += "Diagnostic Generated on "
    file = open("./" + folder + "/date", 'r')
    line = file.readlines()[0]
    string += line + "\n"
    if not 'UTC' in line:
        string += "Center time not in UTC" + "\n" + "\n"

string += "-------------------- System Info --------------------" + "\n" + "\n"

version = ""

if(os.path.isfile(directory + '\\' + folder + '\\' + 'sbs-version')):

    file = open("./" + folder + "/sbs-version", 'r')
    lines = file.readlines()
    version = lines[0][lines[0].index('"')+1:lines[0].rindex('"')] + "." + lines[1][lines[1].index('"')+1:lines[1].rindex('"')] + "." + lines[2][lines[2].index('"')+1:lines[2].rindex('"')] + "+" + lines[3][lines[3].index('"')+1:lines[3].rindex('"')]

    string += "Version: " + version + "\n"
else:
    string += "Version file not found in diag bundle." + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\' + 'center-type')):

    file = open("./" + folder + "/center-type", 'r')
    line = file.readlines()
    file.close()

    string += "Center Type: " + line[0] + "\n"
else:
    string += "Center type file not found in diag bundle." + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\' + 'sbs-extension-list')):

    string += "Extensions:" + "\n"

    file = open("./" + folder + "/sbs-extension-list", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "Extensions file not found in diag bundle." + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\' + 'certificates')):

    string += "Certificates:" + "\n"

    file = open("./" + folder + "/certificates", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "\n" + "Certificates file not found in diag bundle." + "\n" + "\n"

string += "\n" + "-------------------- Network Info --------------------" + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\' + 'ip_addr')):

    string += "IP Address: " + "\n"

    file = open("./" + folder + "/ip_addr", 'r')
    lines = file.readlines()
    file.close()

    found = False

    for line in lines:
        if " eth" in line:
            found = True
        else:
            if "<" in line and ">" in line:
                found = False
        if found:
            string += "\t" + line
else:
    string += "IP address file not found in diag bundle." + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\' + 'ip_link_stats')):
    string += "\n" + "Link Stats:" + "\n"

    file = open("./" + folder + "/ip_link_stats", 'r')
    lines = file.readlines()
    file.close()

    found = False

    for line in lines:
        if " eth" in line:
            found = True
        else:
            if "<" in line and ">" in line:
                found = False
        if found:
            string += "\t" + line
else:
    string += "Link stats file not found in diag bundle." + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\' + 'ip_route')):
    file= open("./" + folder + "/ip_route", 'r')
    lines = file.readlines()
    file.close()

    string += "\n" + "IP Route: " + lines[0] + "\n"
else:
    string += "IP route file not found in diag bundle." + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\conf\\ntp\\ntp.conf')):
    string += "NTP:" + "\n"

    file = open("./" + folder + "/conf/ntp/ntp.conf", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "NTP file not found in diag bundle." + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\conf\\sbs\\sbs-config.json')):
    string += "\n" + "SBS Config: " + "\n"

    file = open("./" + folder + "/conf/sbs/sbs-config.json", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "SBS config file not found in diag bundle." + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\conf\\rsyslog\\backend.conf')):
    string += "\n" + "\n" + "Syslog: " + "\n"

    file = open("./" + folder + "/conf/rsyslog/backend.conf", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line

else:
    string += "\n" + "\n" + "Syslog file not found in diag bundle." + "\n" + "\n"

string += "\n" + "-------------------- Process Info --------------------" + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\top')):

    string += "Top 10: " + "\n"

    file = open("./" + folder + "/top", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        if line.strip()[0:6] == "1 root":
            break
        else:
            string += "\t" + line
else:
    string += "Top 10 file not found in diag bundle." + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\stats\\rabbitmq_queues')):
    string += "\n" + "RabbitMQ Queues: " + "\n"

    file = open("./" + folder + "/stats/rabbitmq_queues", 'r')
    lines = file.readlines()
    file.close()

    warning = ""

    for line in lines:
        string += "\t" + line
        if 'ccv.queue.' in line:
            last = line.rindex('|')
            next = line[:last].rindex('|')
            num = int(line[next+1:last].strip())
            if num > 1:
                warning = line[2:next].strip()
    if len(warning) > 0:
        string += "\n" + "WARNING: " + warning + " has more than one message" + "\n"
else:
    string += "RabbitMQ queues file not found in diag bundle." + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\journal_sbs-marmotd')):

    file = open("./" + folder + "/journal_sbs-marmotd", 'r')
    lines = file.readlines()
    file.close()

    warning = False

    for line in lines:
        if "TIMEOUT" in line or "timeout" in line or "Timeout" in line:
            warning = True
    
    if warning:
        string += "WARNING: Timeout error in journal_sbs-marmotd file" + "\n" + "\n"

string += "\n" + "-------------------- Memory, Storage & DB Info --------------------" + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\memory')):
    string += "Memory:" + "\n"

    file = open("./" + folder + "/memory", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "Memory file not found in diag bundle." + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\filesystem')):
    string += "\n" + "File System:" + "\n"

    file = open("./" + folder + "/filesystem", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "File system file not found in diag bundle." + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\iotop')):
    string += "\n" + "Top 10:" + "\n"

    file = open("./" + folder + "/iotop", 'r')
    lines = file.readlines()
    file.close()

    count = 0
    for line in lines:
        if count < 13:
            string += "\t" + line
        else:
            break
        count += 1
else:
    string += "Top 10 file not found in diag bundle." + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\db\\indexes_size_by_tables')):
    string += "\n" + "DB Index Sizes:" + "\n"

    file = open("./" + folder + "/db/indexes_size_by_tables", 'r')
    lines = file.readlines()
    file.close()

    details = False
    for line in lines:
        if 'details' in line:
            break
        else:
            string += "\t" + line
else:
    string += "DB index sizes file not found in diag bundle."

string += "\n"

string += "\n" + "-------------------- Sensor Info --------------------" + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\sbs_sensor_list')):
    string += "Sensor List:" + "\n"

    file = open("./" + folder + "/sbs_sensor_list", 'r')
    lines = file.readlines()
    file.close()

    enrolled = False
    versions = []
    names = []

    for line in lines:
        string += "\t" + line
        if 'status: ' in line:
            if "ENROLLED" in line:
                enrolled = True
        elif '(serial number=' in line:
            names.append(line[0:line.index("(")-1])
        elif 'version: ' in line:
            versions.append(line[line.index(":")+1:])

    if len(version) > 0:
            for i in range(len(names)):
                if versions[i//2] != version:
                    string += names[i] + " version mismatch" + "\n" + "\n"

    if not enrolled:
        string += "WARNING: Sensor not enrolled" + "\n" + "\n"

else:
    string += "SBS sensor list file not found in diag bundle." + "\n" + "\n"

string += "-------------------- System Configuration --------------------" + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\conf\\ingestion')):
    string += "Data Ingestion:" + "\n"

    file = open("./" + folder + "/conf/ingestion", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "Data ingestion file not found in diag bundle." + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\conf\\custom_networks')):
    string += "Custom Networks:" + "\n"

    file = open("./" + folder + "/conf/custom_networks", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "Custom networks file not found in diag bundle." + "\n" + "\n"

string += "\n" + "\n" + "-------------------- IDS Info --------------------" + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\conf\\snort\\enabled_status')):
    string += "Status:" + "\n"

    file = open("./" + folder + "/conf/snort/enabled_status", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "SNORT status file not found in diag bundle." + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\conf\\snort\\categories')):
    string += "Categories:" + "\n"

    file = open("./" + folder + "/conf/snort/categories", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "SNORT categories file not found in diag bundle." + "\n" + "\n"

now = datetime.now()

current_time = now.strftime("%m-%d-%Y %H-%M-%S")

file_name = "Diagnostic File Report " + current_time + ".txt"

file = open(file_name, 'w')
file.writelines(string)
file.close()

print("Using diag bundle " + folder + ",\nDiagnostic File Report in this directory: " + directory)

time.sleep(5)