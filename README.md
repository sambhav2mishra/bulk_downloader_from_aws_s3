# version 1.0.0
## Description
* This is the initial python script for downloading bulk files from AWS-s3 bucket to local system using subprocess module.
* This script requires and input json file mentioning the file paths in s3.
* This script will work, if you provide valid input json with existing file paths in s3.

## Instruction to run 
* copy AWS environment variables to your terminal.
* sudo apt-get install awscli
* Run python script:
- python3 scripts/download_input_files.py --input input_data/input.json --out output