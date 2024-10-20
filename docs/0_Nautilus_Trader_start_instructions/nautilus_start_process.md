# Guidance for Nautilus Trader installation
Be careful to follow each step in turn.

## Used this  to the Enviroment
<!-- https://docs.nautilustrader.io/developer_guide/environment_setup.html -->

# First update all packages
sudo apt update && sudo apt upgrade

# Ensure in the root user_name/code folder, so 'ls' or 'dir' shows the condorgp folder

# First, cloned from: [lengthy step]
https://github.com/nautechsystems/nautilus_trader

git clone git@github.com:nautechsystems/nautilus_trader.git
cd nautilus_trader

# Create nautilus environment with pyenv
pyenv virtualenv 3.10.6 cgp_naut
# Activate virtualenv locally
pyenv local cgp_naut

## Follow installation instructions
# from:
https://docs.nautilustrader.io/getting_started/installation.html

# install Clang [lengthy step]
sudo apt update && sudo apt upgrade
sudo apt install clang

# Install Rustup [lengthy step]
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
- note, default installation will be fine
# Enable cargo in the current shell:
source $HOME/.cargo/env

# Install poetry
curl -sSL https://install.python-poetry.org | python3 -
# Add poetry to path:
echo -e export PATH="/home/hughharford/.local/bin:$PATH" >> ~/.zshrc
## NOTE: this uses zsh, which might not be your preference...

# Install with poetry [lengthy step]
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


# REVERT BACK TO README instructions... 
