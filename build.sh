#!/bin/bash
apt-get update
apt-get install -y build-essential python3-dev libblas-dev liblapack-dev
pip install -r requirements.txt