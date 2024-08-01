#!/bin/bash

# veracode_api_key_id=<veracode_api_key_id>
# veracode_api_key_secret=<veracode_api_key_secret>

python CreateUsers.py -ID $veracode_api_key_id -key $veracode_api_key_secret -qtd_users 4 -file_name test

# Try to read the credentials file
# file=~/.veracode/credentia ls
# if [[ -r $file ]]; then
#     echo 'file found'
#     $file | grep -A 3 DEFAULT | cut -d '=' -f 2-
# else
#     echo 'file not found'
# fi
# for i in $(seq 1 10);
# do
#     echo $i
# done
# while read -r line; do echo "$line"; done < ~/.veracode/credentials

# if file found, proceed, otherwise, throw 'credential file not found'

# set environment variables equal to credential values 'veracode_api_key_id' and 'veracode_api_key_secret'
