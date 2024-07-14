# Guidance for Nautilus Trader installation
Be careful to follow each step in turn.

## Used this  to the Enviroment
<!-- https://docs.nautilustrader.io/developer_guide/environment_setup.html -->

# First update all packages
sudo apt update && sudo apt upgrade

# First, cloned from:
https://github.com/nautechsystems/nautilus_trader

git clone git@github.com:nautechsystems/nautilus_trader.git
cd nautilus_trader

# Create nautilus environment with pyenv
pyenv virtualenv 3.10.6 naut_trader
# Activate virtualenv locally
pyenv local naut_trader

## Follow installation instructions
# from:
https://docs.nautilustrader.io/getting_started/installation.html

# install Clang
sudo apt update && sudo apt upgrade
sudo apt install clang

# Install Rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
- note, default installation will be fine
# Enable cargo in the current shell:
source $HOME/.cargo/env

# Install poetry
curl -sSL https://install.python-poetry.org | python3 -
# Add poetry to path:
echo -e export PATH="/home/hughharford/.local/bin:$PATH" >> ~/.zshrc
## NOTE: this uses zsh, which might not be your preference...

# Install with poetry
# SKIP THIS___ poetry install --only main --all-extras
#               EXTRAS would include IB Interactive Brokers, for later
# OR just
poetry install

# install pre-commit package
pip install pre-commit

# install pre-commit hook
pre-commit install


### THE ABOVE ALL SEEMED TO WORK WITHOUT HITCH
## Proof will be in whether Nautilus runs

# for Dockerfile, the above did not immediately work:
# trying:
https://docs.nautilustrader.io/developer_guide/environment_setup.html

# Builds
## Following any changes to .pyx or .pxd files, you can re-compile by running:

#                         this seemed to work (certainly different to the above)
poetry run python build.py


## or
make build


# STILL FIND THAT ONCE INSTALLED IN SIDE BY SIDE FOLDER RUNNING ANYTHING
# CONDOR DOESN'T IMMEDIATELY WORK AND CANNOT RECOGNISE/FIND nautilus_trader

- for temporary change to PATH
'''bash
export PATH="~/code/hughharford/nautilus_trader:$PATH"
'''
- didn't work


# INSTALLING FROM CONDORGP LOCATION - NO
'''bash
poetry run python ../nautilus_trader/build.py
'''
gave:
  Poetry could not find a pyproject.toml file in /home/hughharford/code/hughharford/condorgp or its parents

# LOCALLING THE PYENV condorgp virtual environment in the nautilus_trader folder
'''bash
pyenv local condorgp
'''


# THIS IS HOW TO DO IT, CONDORGP RUN CAN NOW FIND nautilus_trader
- Once nautilus fully installed next to condorgp folder:
  local naut_trader env into condorgp folder

'''bash
cd ../condorgp
pyenv local cgp_naut
'''

  reinstalling condorgp in it's own folder, now that the nautilus has been localled
-- WORKED
- Need to give a more considered name to the virtual environment
