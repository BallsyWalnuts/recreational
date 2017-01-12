#! /usr/bin/env python
# encoding: utf-8

import zipfile
import argparse
import time
import os

parser = argparse.ArgumentParser()

parser.add_argument("directory", help="path to directory containing csvs to be zipped")

START_TIME = time.time()

args = parser.parse_args()
os.chdir(args.directory)

for csv in [x for x in os.listdir(args.directory) if ".csv" in x]:
    filename = csv.split(".")[0] + ".zip"
    zip_file = zipfile.ZipFile(filename, "w")
    zip_file.write(csv)
    zip_file.close()
    os.remove(csv)

print(time.time() - START_TIME)
