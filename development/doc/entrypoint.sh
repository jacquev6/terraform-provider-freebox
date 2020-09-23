#!/bin/bash

set -o errexit


# @todo Bypass setup.py
# @todo Remove Link to Travis from left pane. Replace by link to CI action
python setup.py build_sphinx

rm -rf docs
cp -r build/sphinx/html docs

echo
echo "Documentation built"
