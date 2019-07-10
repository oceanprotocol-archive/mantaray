#!/usr/bin/env bash
# Pass in the environment file as the first argument

ENV_FILE=$1

echo "Loading Environment from $ENV_FILE"

while IFS= read -r line
do
  echo "export $line"
  export $line
done < "$ENV_FILE"
#sleep 10

#if [ ! -f $ENV_FILE ]
#then
#  echo "export $(cat ENV_FILE | xargs)"
#fi
#
#env $(cat .env | xargs)