#!/bin/bash

set -o errexit
cd "$(dirname "${BASH_SOURCE[0]}")"

docker build .. --file Dockerfile
image_id=$(docker build --quiet .. --file Dockerfile)

docker run \
    --volume $PWD/test-resources:/terraform-resources \
    --workdir /terraform-resources \
    $image_id \
    bash -c "terraform providers && echo && terraform init && echo && terraform apply"
