# CS4575_project_1

## Venv setup

Install [EnergiBridge](https://github.com/tdurieux/EnergiBridge) first, instructions are below.

Create the environment with

`python -m venv ./venv`

Activate the Python virtual environment:

Windows: `venv\Scripts\activate`

Mac: `source venv/bin/activate`

Install [PyEnergiBridge](https://github.com/luiscruz/pyEnergiBridge):

`pip install git+https://github.com/luiscruz/pyEnergiBridge.git`

Install remaining packages:

`pip install -r requirements.txt`

## Installing EnergiBridge on Winwdows

In the `bin` folder you can find the required files. Make sure to run the commands in an Administrator cmd (not PowerShell) shell in the project directory.

Create service:

`sc create rapl type=kernel binPath="<absolute path to LibreHardwareMonitor.sys in bin folder>"`

Start service:

`sc start rapl`

Make a copy of the `pyenergibridge_config.json.example` file and name it `pyenergibridge_config.json`. Edit the absolute path to the energibridge executable (energibridge.exe) in the file. Something like `C:\Users\Name\blablabla\bin\energibridge.exe`.

To test if it works:

`bin\energibridge.exe -o results.csv --summary timeout 3`

If you want to stop the service for some reason:

`sc stop rapl`

To remove the service after the course is over:

`sc delete rapl`
