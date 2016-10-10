#!/usr/bin/env python
import update_package

f = open('packages', 'r')

for package in f:
    update_package.update(package)
    print package
