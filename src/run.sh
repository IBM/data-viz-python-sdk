#!/usr/bin/env bash

#===============================================================
# IBM Confidential
#
# OCO Source Materials
#
# Copyright IBM Corp. 2018
#
# The source code for this program is not published or otherwise
# divested of its trade secrets, irrespective of what has been
# deposited with the U.S. Copyright Office.
#===============================================================

DATA_LOCATION=/data/datafiles/

MODEL_VERSION=$(echo $VERSION | cut -d "." -f 1,2)

export AWS_ACCESS_KEY_ID=$S3FS_ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=$S3FS_SECRET_KEY

# Load data into a pandas dataframe
echo "Starting: Call Amhairc Library"
python3 /opt/amhairc.py
if [ $? != "0" ]
then
  >&2 echo "Failed to call Amhairc Library"
  exit 1
fi
echo "Finished: Call to Amhairc Library"









