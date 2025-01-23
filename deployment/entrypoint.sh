#!/bin/bash

# Extract the password from restapi.secret
PASSWORD=$(grep 'default' /opt/domjudge/domserver/etc/restapi.secret | awk '{print $NF}')
echo "PASSWORD"
echo $PASSWORD

if [ -z "$PASSWORD" ]; then
  echo "Failed to extract the password from restapi.secret"
  exit 1
fi

# Export the password as an environment variable
export JUDGEDAEMON_PASSWORD=$PASSWORD
echo "JUDGEDAEMON_PASSWORD=$PASSWORD" > /judgehost.env  # Write to a shared directory

exit 0
