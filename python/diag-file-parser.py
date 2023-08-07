from pathlib import Path
import time
from datetime import datetime

folder = input("Please input the name of your diag folder: ")

while len(folder) == 0 or len(folder.replace(" ", "")) == 0:
    folder = input("Please input the name of your diag folder: ")

file = open("./" + folder + "/center-type", 'r')
line = file.readlines()
file.close()

string = "----- System Info -----" + "\n" + "\n" + "Center Type: " + line[0] + "\n" + "Extensions:" + "\n"

file = open("./" + folder + "/sbs-extension-list", 'r')
lines = file.readlines()
file.close()

for line in lines:
    string += line

string += "\n" + "----- Network Info -----" + "\n" + "\n" + "IP Address: " + "\n"

file = open("./" + folder + "/ip_addr", 'r')
lines = file.readlines()
file.close()

start = -1
end = -1

for i in range(len(lines)):
    line = lines[i]
    if line[0] == "2":
        start = i
    elif line[0] == "4":
        end = i
    if start != -1 and end == -1:
        string += "\t" + line

string += "\n" + "Link Stats:" + "\n"

file = open("./" + folder + "/ip_link_stats", 'r')
lines = file.readlines()
file.close()

start = -1
end = -1

for i in range(len(lines)):
    line = lines[i]
    if line[0] == "2":
        start = i
    elif line[0] == "4":
        end = i
    if start != -1 and end == -1:
        string += "\t" + line

file= open("./" + folder + "/ip_route", 'r')
lines = file.readlines()
file.close()

string += "\n" + "IP Route: " + lines[0] + "\n" + "NTP:" + "\n"

file = open("./" + folder + "/conf/ntp/ntp.conf", 'r')
lines = file.readlines()
file.close()

for line in lines:
    string += "\t" + line

string += "\n" + "SBS Config: " + "\n"

file = open("./" + folder + "/conf/sbs/sbs-config.json", 'r')
lines = file.readlines()
file.close()

for line in lines:
    string += "\t" + line

string += "\n" + "\n" + "Syslog: " + "\n"

file = open("./" + folder + "/conf/rsyslog/backend.conf", 'r')
lines = file.readlines()
file.close()

for line in lines:
    string += "\t" + line

string += "\n" + "----- Process Info -----" + "\n" + "\n" + "Top 10: " + "\n"

file = open("./" + folder + "/top", 'r')
lines = file.readlines()
file.close()

for line in lines:
    if line.strip()[0:6] == "1 root":
        break
    else:
        string += "\t" + line

string += "\n" + "RabbitMQ Queues: " + "\n"

file = open("./" + folder + "/stats/rabbitmq_queues", 'r')
lines = file.readlines()
file.close()

for line in lines:
    string += "\t" + line

string += "\n" + "----- Memory, Storage & DB Info -----" + "\n" + "\n" + "Memory:" + "\n"

file = open("./" + folder + "/memory", 'r')
lines = file.readlines()
file.close()

for line in lines:
    string += "\t" + line

string += "\n" + "File System:" + "\n"

file = open("./" + folder + "/filesystem", 'r')
lines = file.readlines()
file.close()

for line in lines:
    string += "\t" + line

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

string += "\n" + "----- Sensor Info -----" + "\n" + "\n" + "Sensor List:" + "\n"

file = open("./" + folder + "/sbs_sensor_list", 'r')
lines = file.readlines()
file.close()

for line in lines:
    string += "\t" + line

string += "----- System Configuration -----" + "\n" + "\n" + "Data Ingestion:" + "\n"

file = open("./" + folder + "/conf/ingestion", 'r')
lines = file.readlines()
file.close()

for line in lines:
    string += "\t" + line

string += "Custom Networks:" + "\n"

file = open("./" + folder + "/conf/custom_networks", 'r')
lines = file.readlines()
file.close()

for line in lines:
    string += "\t" + line

string += "\n" + "\n" + "----- IDS Info -----" + "\n" + "\n" + "Status:" + "\n"

file = open("./" + folder + "/conf/snort/enabled_status", 'r')
lines = file.readlines()
file.close()

for line in lines:
    string += "\t" + line

string += "Categories:" + "\n"

file = open("./" + folder + "/conf/snort/categories", 'r')
lines = file.readlines()
file.close()

for line in lines:
    string += "\t" + line

now = datetime.now()

current_time = now.strftime("%m-%d-%Y %H-%M-%S")

file_name = "Diagnostic File Report " + current_time + ".txt"

file = open(file_name, 'w')
file.writelines(string)
file.close()

print("Diagnostic File Report in this directory: " + str(Path.cwd()))

time.sleep(5)