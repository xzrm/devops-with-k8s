#!/bin/bash

#Trim quates if present
export BACKEND_BASE_URL=$(echo "$BACKEND_BASE_URL"| sed 's/^"\(.*\)"$/\1/')

for file in $JSFOLDER;
do
  cat $file | envsubst '${BACKEND_BASE_URL}' | tee $file
done

