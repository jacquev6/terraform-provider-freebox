FROM python:3.8

RUN curl -O https://releases.hashicorp.com/terraform/0.12.29/terraform_0.12.29_linux_amd64.zip \
 && unzip terraform_0.12.29_linux_amd64.zip \
 && mv terraform /usr/local/bin/ \
 && rm terraform_0.12.29_linux_amd64.zip

# Make "pip install" steps quicker by pre-installing dependencies
RUN pip install protobuf grpcio cryptography u-msgpack-python requests

# @todo Install from PyPI (when Pyrraform is stable)
COPY Pyrraform/src /Pyrraform
RUN pip install /Pyrraform

COPY terraform-provider-freebox /terraform-provider-freebox
RUN pip install /terraform-provider-freebox
