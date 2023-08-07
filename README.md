# Cisco Cyber Vision API Scripts

This is a collection of Python scripts with Cyber Vision API queries to generate custom reports.   

These files must be run on a Windows device with IP access to the Cyber Vision Center.  It will prompt for a valid API key and IP address of CV Center.

Files will be output to the current working directory where the scripts are executed.

## Requirements
There are two methods that can be used to run these python scripts on a Windows host:
1. Download & install Python from Python.org and install it on your Windows host
2. Package the scripts as standalone .EXE files using Pyinstaller (see below)

## File Descriptions

```cred-var-separated```: This file will generate an Excel file with a credentials and variables report with separate worksheets for devices and components.

```cred-var```: This file will generate a report with only two worksheets: Credentials and Variables. The values for both devices and components will be on the same worksheet.

```find-kevs```: This file will generate an HTML report of the known exploited vulnerabilities on your network. You must use Cyber Vision to generate a vulnerability report and put that CSV report in the same directory as this file when you run it.

```security-insights```: This file will generate a security insights summary report.

```security-insights-details```: This file will generate a detailed security insights report for DNS, HTTP & SMB with individual component details and request counts.

```diag-file-parser```: This file will generate a summary report of key items from a complete Cyber Vision Center diagnostic bundle.  

  **Instructions:** 
  1) Generate and download a diagnostic bundle from the Cyber Vision Center
  2) Unpack the .tgz diagnostic bundle, then unpack the .tar archive, which will result in a folder named 'sbs-diag-export-*yyyymmddhhmmss*'. 
  3) Execute this utility from the same directory where you placed the diagnostic bundle
  4) When the utility completes, a summary report will be saved as a .txt file to the same directory.

## Make Your Own Executables

If you're interested in making your own executables, you can use [Pyinstaller](https://pypi.org/project/pyinstaller/).
