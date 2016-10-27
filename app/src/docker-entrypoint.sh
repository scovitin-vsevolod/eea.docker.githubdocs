#!/usr/bin/env bash

if [ ! -e /root/.ssh/known_hosts ]; then
  ssh-keyscan github.com > /root/.ssh/known_hosts
fi

if [[ "$1" == "http"* ]] || [[ "$1" == "git@"* ]]; then
  exec python update_package.py "$@"
fi

exec "$@"
