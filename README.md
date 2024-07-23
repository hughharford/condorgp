[![Build Status](https://dev.azure.com/hughharford/CONDOR_GP/_apis/build/status%2Fhughharford.condorgp?branchName=refs%2Fpull%2F17%2Fmerge)](https://dev.azure.com/hughharford/CONDOR_GP/_build/latest?definitionId=1&branchName=refs%2Fpull%2F17%2Fmerge)

# About CondorGP
- This is a highly ambitious Fintech AI project.
- Description: the AI used is not Deep Learning (although NNs will be used),
at the high level, genetic programming (GP) is the approach.
- - GP outputs are live code, and GP is well known for athropomorphised
    ingenuity and cleverness.
- Data Source: various, including quant market history, for initial hypothesis
- Type of analysis: backtested evolving algorithms created by DEAP, with fitness function specified by GP. Backtesting undertaken by Nautilus Trader.

# Startup the project
The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Once you have setup your ssh public key...

# Get CondorGP (via SSH if that is setup)
```bash
git clone git@github.com:hughharford/condorgp.git
```
as per the above but replace this line for HTTPS (not got SSH setup):
```bash
git clone https://github.com/hughharford/condorgp.git
```

# This will fail, now
Follow the instructions in:
docs/0_Nautilus_Trader_start_instructions/nautilus_start_process.md

#  Once Nautilus_trader folder in place next to condorgp

# Enable CondorGP in side by side folder to see nautilus_trader
- Once nautilus fully installed next to condorgp folder:
  local naut_trader env into condorgp folder

'''bash
cd ../condorgp
pyenv local cgp_naut
pip install -r requirements
'''

# Functional test with a script
```bash
# cd condorgp - should be here already
make install test
# OR
pytest
```
