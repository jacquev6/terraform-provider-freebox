#!/bin/bash

set -o errexit

rm -rf docs
python setup.py build_sphinx
cp -r build/sphinx/html docs

echo
echo "Documentation built"
