[![Build Status](https://dev.azure.com/hughharford/CONDOR_GP/_apis/build/status%2Fhughharford.condorgp?branchName=refs%2Fpull%2F17%2Fmerge)](https://dev.azure.com/hughharford/CONDOR_GP/_build/latest?definitionId=1&branchName=refs%2Fpull%2F17%2Fmerge)

# About CondorGP
- This is a highly ambitious Fintech AI project. 
- Description: genetic programming
- Data Source: various tbc, expected quant market history only, for initial hypothesis
- Type of analysis: backtested evolving algorithms created by DEAP, with fitness function specified by us.

# Startup the project
The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```
Unittest test:
```bash
make clean install test
```

STANDARD BOILERPLATE FROM HERE DOWN >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
' >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Check for condorgp in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/condorgp`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "condorgp"
git remote add origin git@github.com:{group}/condorgp.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
condorgp-run
```

# Install

Go to `https://github.com/{group}/condorgp` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/condorgp.git
cd condorgp
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
condorgp-run
```
