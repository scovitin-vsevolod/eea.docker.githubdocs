#!/usr/bin/env bash

# Add github to known_hosts
if [ ! -e /root/.ssh/known_hosts ]; then
  mkdir -p /root/.ssh
  ssh-keyscan github.com > /root/.ssh/known_hosts
  chmod 0700 /root/.ssh
fi

# SSH key
if [ ! -e /root/.ssh/id_rsa ]; then
  if [ -e /src/id_rsa ]; then
    cp /src/id_rsa /root/.ssh/
    chmod 0600 /root/.ssh/id_rsa
  fi
fi

# Generate docs
if [[ "$1" == "http"* ]] || [[ "$1" == "git@"* ]]; then
  exec python update_package.py "$@"
fi

# Anything else
exec "$@"
