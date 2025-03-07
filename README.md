# AgenticAIIsh
For precticing Agentic AI

# Setup Instructions

## Prerequisites

* Python
* OpenAI API KEY/Local running model
* pvenv
* crewAI

## Step 1: Installation

* Install Python verion > 13.0 
* In case you have multiple versions installed then you can you pvenv by referring followinfg steps:
* Open PowerShell as Administrator.
* Run the following command to clone pyenv-win:
git clone https://github.com/pyenv-win/pyenv-win.git $env:USERPROFILE\.pyenv
* Add pyenv to your system environment variables:
    * Open Start and search for "Environment Variables".
    * Under System Variables, find Path and click Edit.
    * Click New and add the following paths:
%USERPROFILE%\.pyenv\pyenv-win\bin
%USERPROFILE%\.pyenv\pyenv-win\shims
    * Click OK to save.
* Check if pyenv is working:
pyenv --version
* Install a specific version:
    pyenv install 3.x.x
* List all versions of python:
    pyenv install --list
* Set the global or local version:
pyenv global 3.x.x  # Set for all users
pyenv local 3.x.x   # Set for the current directory/project

* If VSCode still shows wrong version then:
* Change Python Interpreter in VS Code:
    1. Press Ctrl + Shift + P to open the Command Palette.
    2. Search for "Python: Select Interpreter" and click it.
    3. Look for the version managed by pyenv (it should be in a path like C:\Users\YourUser\.pyenv\pyenv-win\versions\3.11.x).
* Select the correct version and restart VS Code.

## Step 2: Configuration

* Follwo the steps mentioned in https://docs.crewai.com/quickstart

## Step 3: Verification

* Try running the code in VSCode

## Troubleshooting

* Enable verbose


## Next Steps

* TBA