# Python: a second chance

## pyenv
pyenv manages the versions of Python. Use pyenv to
-> install new versions
-> decide which version to use globally or locally

pyenv has configuration in ~/.zshrc and in ~/.pyenv, where it will store the installed python versions.
After setting up pyenv and the preferred version of python, running `python` or `pip` will use the pyenv-provided version.

## venv (virtual environment)
In the desired project directory:
- `python -m venv <env_name>` -> will create a <env_name> subfolder with plenty of stuff inside
- `source <env_name>/bin/activate` -> will open a sub-shell specific to this virtual environment
- `deactivate` to exit the venv
=> "Now that you have an activated virtual environment, any Python packages you install will be isolated within this environment."

## pip
Package manager, installs python libraries (should be installed within the venv).
- `pip install package-name`
- `pip freeze > requirements.txt`
- `pip install -r requirements.txt`

## Network
- `minikube tunnel`
- open in browser: http://192.168.64.2:30000/docs