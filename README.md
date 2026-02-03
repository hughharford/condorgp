[![Build Status](https://dev.azure.com/hughharford/CONDOR_GP/_apis/build/status%2Fhughharford.condorgp?branchName=refs%2Fpull%2F17%2Fmerge)](https://dev.azure.com/hughharford/CONDOR_GP/_build/latest?definitionId=1&branchName=refs%2Fpull%2F17%2Fmerge)

# About CondorGP
- This is a highly ambitious Fintech AI project.
- Description: the AI used is not Deep Learning (although NNs will be used),
at the high level, genetic programming (GP) is the approach.
- - GP outputs are live code, and GP is well known for athropomorphised
    ingenuity and cleverness.
- Data Source: various, including quant market history, for initial hypothesis
- Type of analysis: backtested evolving algorithms created by DEAP, with fitness function specified by GP. Backtesting undertaken by Nautilus Trader.

# Install the project
- First update all packages
```bash
sudo apt update && sudo apt upgrade
```
- Install poetry, with specific version:
```bash
pipx install poetry==1.8.4
```
- Ensure you have setup your ssh public key...
- Then clone the repo
```bash
git clone git@github.com:hughharford/condorgp.git
```

# poetry install

# This will fail, now
Follow the instructions in:
docs/0_Nautilus_Trader_start_instructions/nautilus_start_process.md

#  Once Nautilus_trader folder in place next to condorgp
- Check nautilus can be run from CondorGP
```bash
poetry run python ./condorgp/evaluation/run_naut.py
```
- If this runs many lines of output, it's working


# Functional test with a script
```bash
# cd condorgp - should be here already
make install test
# OR
pytest
```

# For contributors, do a -e installation to allow updates based on your changes
```bash
# cd condorgp - should be here already
pip install -e .
```
