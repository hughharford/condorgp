#!/bin/bash
## for use on CGP container to reclone code fast

# get to code folder
cd ~/code
# clear old repo
rm -rf condorgp
# reclone single branch
git clone --single-branch https://github.com/hughharford/condorgp.git

cd condorgp
# install again to be sure
make install

cd ~/code/condorgp/
