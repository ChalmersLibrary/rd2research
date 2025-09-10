#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script for uploading RD project file to Azure Fileshare
# req: pip3 install azure-storage-file-share
# https://learn.microsoft.com/en-us/python/api/overview/azure/storage-file-share-readme?view=azure-python

import sys
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
from azure.storage.fileshare import ShareFileClient

load_dotenv()

d = datetime.now()
current_date = d.strftime("%Y-%m-%dT%H:%M:%S.%f")

# Create a logger for the 'azure.storage.fileshare' SDK
logger = logging.getLogger('azure.storage.fileshare')
logger.setLevel(logging.DEBUG)

# Configure a console output
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
logfile=os.getenv("LOG_FILE")
# use logging_enabled=True to enable

file=os.getenv("LOCAL_FILE")
file_client = ShareFileClient.from_connection_string(conn_str=os.getenv("CONN_STRING"), share_name=os.getenv("SHARE_NAME"), file_path=os.getenv("FILE_PATH"),logging_enable=False)

# Upload file
try:
    with open(file, "rb") as source_file:
        file_client.upload_file(source_file)
    with open(logfile, "a") as f:
        print(str(current_date) + ": File uploaded successfully!", file=f)
except:
    e = sys.exc_info()[0]
    with open(logfile, "a") as f:
        print(str(current_date) + ': File could not be uploaded: %s' % e)
    exit()
