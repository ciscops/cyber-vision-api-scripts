# Cisco Cyber Vision API Scripts

These .exe files must be run on a device that can access the Cyber Vision Center.  It will prompt for a valid API key and IP address of CV Center.

Files will be output to the current working directory where the scripts are executed.

## File Descriptions

```cred-var-separated.exe```: This file will generate a credentials and variables report with separate worksheets for devices and components.

```cred-var.exe```: This file will generate a report with only two worksheets: Credentials and Variables. The values for both devices and components will be on the same worksheet.

```find-kevs.exe```: This file will generate an HTML report of the known exploited vulnerabilities on your network. You must use Cyber Vision to generate a vulnerability report and put that CSV report in the same directory as this file when you run it.

```security-insights-details.exe```: This file will generate a security insights report where each DNS, HTTP, or SMB is further separated by component and its request count.

```security-insights.exe```: This file will generate a security insights report which does not include details about the components related to DNS, HTTP, or SMB.
