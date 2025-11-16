#!/bin/bash

# Script to automatically pull the latest changes
# from the node_steward repository
cd ~/node_steward
git fetch && git pull origin main
