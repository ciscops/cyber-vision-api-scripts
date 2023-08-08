from pathlib import Path
import time
from datetime import datetime
import os

folders = []

folder = ""

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
        print("Diag bundle " + folder + " not found.")
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

directory = str(Path.cwd())
print(directory)

string = "-------------------- System Info --------------------" + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\' + 'center-type')):

    file = open("./" + folder + "/center-type", 'r')
    line = file.readlines()
    file.close()

    string += "Center Type: " + line[0] + "\n"
else:
    string += "Center type file not found" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\' + 'sbs-extension-list')):

    string += "Extensions:" + "\n"

    file = open("./" + folder + "/sbs-extension-list", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += line
else:
    string += "Extensions file not found" + "\n"

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
    string += "IP address file not found" + "\n"

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
    string += "Link stats file not found" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\' + 'ip_route')):
    file= open("./" + folder + "/ip_route", 'r')
    lines = file.readlines()
    file.close()

    string += "\n" + "IP Route: " + lines[0] + "\n"
else:
    string += "IP route file not found" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\conf\\ntp\\ntp.conf')):
    string += "NTP:" + "\n"

    file = open("./" + folder + "/conf/ntp/ntp.conf", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "NTP file not found" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\conf\\sbs\\sbs-config.json')):
    string += "\n" + "SBS Config: " + "\n"

    file = open("./" + folder + "/conf/sbs/sbs-config.json", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "SBS config file not found" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\conf\\rsyslog\\backend.conf')):
    string += "\n" + "Syslog: " + "\n"

    file = open("./" + folder + "/conf/rsyslog/backend.conf", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line

else:
    string += "Syslog file not found" + "\n"

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
    string += "Top 10 file not found" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\stats\\rabbitmq_queues')):
    string += "\n" + "RabbitMQ Queues: " + "\n"

    file = open("./" + folder + "/stats/rabbitmq_queues", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "RabbitMQ queues file not found" + "\n"

string += "\n" + "-------------------- Memory, Storage & DB Info --------------------" + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\memory')):
    string += "Memory:" + "\n"

    file = open("./" + folder + "/memory", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "Memory file not found" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\filesystem')):
    string += "\n" + "File System:" + "\n"

    file = open("./" + folder + "/filesystem", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "File system file not found" + "\n"

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
    string += "Top 10 file not found" + "\n"

string += "\n" + "-------------------- Sensor Info --------------------" + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\sbs_sensor_list')):
    string += "Sensor List:" + "\n"

    file = open("./" + folder + "/sbs_sensor_list", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "SBS sensor list file not found" + "\n"

string += "-------------------- System Configuration --------------------" + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\conf\\ingestion')):
    string += "Data Ingestion:" + "\n"

    file = open("./" + folder + "/conf/ingestion", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "Data ingestion file not found" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\conf\\custom_networks')):
    string += "Custom Networks:" + "\n"

    file = open("./" + folder + "/conf/custom_networks", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "Custom networks file not found" + "\n"

string += "\n" + "\n" + "-------------------- IDS Info --------------------" + "\n" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\conf\\snort\\enabled_status')):
    string += "Status:" + "\n"

    file = open("./" + folder + "/conf/snort/enabled_status", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "SNORT status file not found" + "\n"

if(os.path.isfile(directory + '\\' + folder + '\\conf\\snort\\categories')):
    string += "Categories:" + "\n"

    file = open("./" + folder + "/conf/snort/categories", 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        string += "\t" + line
else:
    string += "SNORT categories file not found" + "\n"

now = datetime.now()

current_time = now.strftime("%m-%d-%Y %H-%M-%S")

file_name = "Diagnostic File Report " + current_time + ".txt"

file = open(file_name, 'w')
file.writelines(string)
file.close()

print("Using diag bundle " + folder + ", Diagnostic File Report in this directory: " + directory)

time.sleep(5)