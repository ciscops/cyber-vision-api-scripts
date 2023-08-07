# Cisco Cyber Vision API Scripts

This is a collection of Python scripts with Cyber Vision API queries to generate custom reports.  The Python scripts are packaged as standalone executables that will run on Windows workstations, so there is no need to install Python on the Cyber Server or on the Windows workstation. 

These .exe files must be run on a Windows device with IP access to the Cyber Vision Center.  It will prompt for a valid API key and IP address of CV Center.

Files will be output to the current working directory where the scripts are executed.

## File Descriptions

```cred-var-separated.exe```: This file will generate an Excel file with a credentials and variables report with separate worksheets for devices and components.

```cred-var.exe```: This file will generate a report with only two worksheets: Credentials and Variables. The values for both devices and components will be on the same worksheet.

```find-kevs.exe```: This file will generate an HTML report of the known exploited vulnerabilities on your network. You must use Cyber Vision to generate a vulnerability report and put that CSV report in the same directory as this file when you run it.

```security-insights-details.exe```: This file will generate a detailed security insights report for DNS, HTTP & SMB with individual component details and request counts.

```security-insights.exe```: This file will generate a security insights summary report.
