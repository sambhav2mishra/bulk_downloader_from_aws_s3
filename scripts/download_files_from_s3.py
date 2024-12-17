import json
import argparse
import logging
import subprocess
import os

logging.basicConfig(level=logging.INFO, filename="logData.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s", datefmt="%m/%d/%Y %H:%M:%S %Z")
logger = logging.getLogger(__name__)

VERSION = 'VERSION: 1.0.0'
AUTHOR = "Smruti Sambhav Mishra"
logger.info(f"Developed by {AUTHOR}")
logger.info(VERSION)

'''
This script downloads all the files present in aws s3 bucket except large files like bam, sam and fasta etc
'''

def run_job(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
        logger.info('Command: {0} ran successfully.'.format(cmd))
    except subprocess.CalledProcessError as e:
        logger.error('Failed to run: {0}. '.format(cmd) + str(e))
        exit(1)

def get_file_size(file):
    try:
        cmd = "aws s3 ls {0} --recursive --human-readable --summarize | grep 'Total Size' | awk '{{print $3, $4}}'".format(file)
        size = subprocess.getoutput(cmd)
        return size
    except Exception as e:
        logger.error(e)
        exit(1)

def main(args):
    try:
        logger.info("Reading input JSON file...")
        with open(args.input,"r") as infile:
            data = json.load(infile)
            logger.info("Creating output directory...")
            out_dir = args.out
            if os.path.exists(out_dir):
                logger.info("output folder exists")
            else:
                run_job(f"mkdir -p {out_dir}")
            for key, path in data.items():
                if path.startswith("s3"):
                    splited_path = path.split("/")
                    if splited_path[-1].endswith((".bam", ".bam.bai", ".fa", ".fasta", ".sam")):
                        logger.warning(f"Skipping {splited_path[-1]} file for download because of huge size -> {get_file_size(path)} ")
                    else:
                        run_job(f"aws s3 cp {path} {out_dir}")
                        
            logger.info(f"All the files are downloaded under this directory {out_dir}")

    except Exception as e:
        logger.error(e)
        exit(1)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Download bulk files from AWS-s3 bucket")
    parser.add_argument("--input", type=str, required=True, help="Input will be a json file for sample please view input_data")
    parser.add_argument("--out", type=str, required=False, default="output", help="output path")
    args = parser.parse_args()
    main(args)