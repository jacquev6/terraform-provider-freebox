#!/bin/bash

set -o errexit
cd "$(dirname "${BASH_SOURCE[0]}")"

do_create_token=false
while [[ "$#" -gt 0 ]]
do
  case $1 in
    --create-token)
      do_create_token=true
      ;;
    *)
      echo "Unknown parameter passed: $1"
      exit 1;;
  esac
  shift
done

image_id=$(docker build --quiet ../../.. --file Dockerfile)

rm -rf \
  resources/terraform.tfstate \
  resources/.terraform \
  resources/terraform-provider-freebox.log

if $do_create_token
then
  docker run \
    --env DEBUG_TERRAFORM_PROVIDER_FREEBOX=true \
    --volume $PWD/resources:/terraform-resources \
    --workdir /terraform-resources \
    $image_id \
    terraform-provider-freebox create-token \
      --app-id terraform-provider-freebox-tests \
      --app-name "Tests for terraform-provider-freebox" \
      --app-version "dev" \
      --device-name $(hostname)
  read -p "Press 'Enter' when done"
fi

docker run \
  --env DEBUG_TERRAFORM_PROVIDER_FREEBOX=true \
  --volume $PWD/resources:/terraform-resources \
  --workdir /terraform-resources \
  $image_id \
  bash -c "terraform providers && echo && terraform init && echo && terraform apply"
