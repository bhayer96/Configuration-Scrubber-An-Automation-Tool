# Configuration Scrubber: An Automation Tool
This repository consists of an automation tool that scrubs customer sensitive data from network configurations and some sample input and output for the program. Sensitive data could be descriptions, IP addresses, passwords, key-strings, or SNMP-servers. This tool makes the process of scrubbing configurations much quicker and simpler. The first phase of this tool is written to Hide.py, while the second version is written to Scrub.py.
## Set Up of Environment
### Software Requirements
The Python script has been coded according to Python 2.7.x standards. Some code may cause errors if the script is run in a non-Python 2.7.x based environment. 
### Installation
Check to see what version of Python is on your environment. You can easily do this through the following steps:
```
$ python --version
Python 2.7.10
```
If Python 2.7.x is not installed in your environment, install it using Homebrew.
First, to install Homebrew, run the following on Terminal:
```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Follow the instructions the script gives you to complete the installation of Homebrew. Once it has been installed, insert the Homebrew directory at the top of your **PATH** environment. To do this, add the following to the bottom of your ~/.profile file.
```
export PATH=/usr/local/bin:/usr/local/sbin:$PATH
```
Install Python 2.7 by running the following:
```
$ brew install python
```

Now, you can download the [Configuration Scrubber](https://github.com/bhayer96/Configuration-Scrubber-An-Automation-Tool) repository.
## Run the Script
In Terminal, navigate to the repository's directory on your system. Once there, run the following to start the program:
```
$ python Scrub.py
```
If you do not already have one, type in the name of the sample input network configuration file when prompted.
```
Please enter file name, including the file extension.
>>   ASR-1K-A_running-config.txt
```
From there, choose an item to scrub from the menu provided. A sample run of this would be:
```
Type in data type to scrub or an action to complete using the menu below:

Description:		de
IP Address:		ip
Key-string:		ks
Password:		pw
Snmp-server:		ss
Display original:	do
Display scrubbed:	ds
Quit:			qu

>>   de
```
Continue playing with menu until you wish to quit. Depending on what you scrubbed, there should be either one or two output files. If you chose to scrub IP addresses, then there will be two new files.
