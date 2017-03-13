#!/bin/bash

if [ ! -f medicinelist.csv ]; then
        python2 initialsync.py
fi
python2 sync.py
python2 database.py

