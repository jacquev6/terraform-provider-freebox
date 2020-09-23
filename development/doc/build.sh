#!/bin/bash

set -o errexit
cd "$(dirname "${BASH_SOURCE[0]}")"


image_id=$(
  docker build \
    --quiet \
    .
)

cd ../..

docker run \
  --rm \
  --volume $PWD:/project \
  --workdir /project \
  $image_id
