# ExportContacts tool

## Overview

`ExportContacts tool` is a simple email analytics application that looks for all the e-mails in your Sent Items folder (both in your main Exchange mailbox and in the online archive) that were sent to recipients. The application produces an Excel file with the list of recipients along with the date and subject of the latest email that was sent to a particular recipient.

## Installing

Build bundle running one of files in the `scripts/` folder(build_exe.bat for Windows and build_dmg.sh for MacOS). Scripts automatically creates .exe or .dmg file(depends on your OS), and you should just run this file. Currently, Windows and macOS(minimum version: 10.13 High Sierra) are supported.

## Usage

Launch `ExportContacts tool.exe` (Windows) or `ExportContacts tool.app` (macOS).

Type your username, email, and password in the form (**please pay attention here as your mailbox can use a different spelling than your user name**). Also, you should read terms and policies and agree with them to be able to export data from your mailbox. There is a possibility to exclude some email domains that you don't want to export.

Finally, if the user name, the password, and the mailbox are correct, and the script was able to connect to your Exchange mailbox, you will be able to choose a directory where to export data. As a result, you will see a PopUp message at the window. The exported data can be found in <user<span>.name>_<day-month-year_hour_minute>_contacts.xlsx file.

## Development

### Automatic Setup
_If you are using Windows, Python 3.7 must be installed before running .bat file_
For successful setup run **setup_project.bat** (for Windows) or **setup_project.sh** (for macOS). 

##### For setup project on Windows open cmd and run:

`setup_project.bat`

##### For setup project on MacOS open Terminal and run:

`sudo chmod +x setup_project.sh` - give permission for execution

`./setup_project.sh` - execute file with auto setup

This file will automatically download and install all the dependencies. You can read the whole list of dependencies below, in the Manual Setup section and Pipfile for Python dependencies.

Or you can manually set up the project.

### Prerequisites

- Python 3.7

- pyenv (pyenv-win on Windows)

- pipenv

### Manual Setup

1. Install Python 3. Python 3.7 is preferable but other 3.x versions should generally work fine because the global version is only used to install and run pyenv and pipenv.
2. install pyenv / pyenv-win by carefully following the installation instructions (*especially important on Windows where extra manual steps are needed!*)
3. install pipenv
4. Clone the git repository 
5. Open command prompt / terminal and `cd` to the directory where you have cloned the repository
6. Type `env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install -k -v 3.7.5` (on macOS) or  `pyenv install 3.7.5-amd64` (on Windows). Please note that *on macOS, this will lead to building Python from sources, so the installation process could take some time*.
7. Type `pipenv install --dev`

Now, you should be ready to go!

### Saving Your Credentials So You Don't Have to Enter It Every Time
If you checked checkbox for saveing credentials, the application will save your email_service_address, username, email and password in Windows Credential Manager or MacOs keychain after first success export contacts. In the future, these credentials will be automatically entered into the user input form. You can retrieve your credentials in Windows Credential Manager or MacOs keychain with the names ExportContacts_email_service_address, ExportContacts_username, ExportContacts_email, ExportContacts_password.

### Run project
For running project just type `python main.py`.

### Log mode
In the command prompt, you can launch the application with an argument `--logging` and all processes that run inside the program logic will be recorded in the `history.log` file.

### Tests
Unit test have been written for this project. To run these tests enter the `src` directory and type:
`python -m pytest`

## Contributing

This project is not being actively supported. To develop `ExportContacts tool`, please fork this repository and work from there.
