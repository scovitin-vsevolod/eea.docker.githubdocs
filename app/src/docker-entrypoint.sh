#!/usr/bin/env bash

# Add github to known_hosts
if [ ! -e /root/.ssh/known_hosts ]; then
  mkdir -p /root/.ssh
  ssh-keyscan github.com > /root/.ssh/known_hosts
  chmod 0700 /root/.ssh
fi

# SSH key from SSH_KEY env
if [ ! -e /root/.ssh/id_rsa ]; then
  if [ ! -z "$SSH_KEY" ]; then
    echo "$SSH_KEY" > /root/.ssh/id_rsa
    chmod 0600 /root/.ssh/id_rsa
  fi
fi

# Generate all docs: --repo REPO --skip SKIP
if [[ "$1" == "-"* ]]; then
  exec python update_all.py "$@"
fi

# Generate docs
if [[ "$1" == "http"* ]] || [[ "$1" == "git@"* ]]; then
  exec python update_package.py "$@"
fi

# Anything else
exec "$@"
