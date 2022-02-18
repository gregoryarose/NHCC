#!/bin/bash

echo "NHCC standby ........"

cd "NHCC"
python3 NHCCRiderHistory.py 


kill $PPID 
