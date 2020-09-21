FROM python:3

RUN curl -O https://releases.hashicorp.com/terraform/0.12.29/terraform_0.12.29_linux_amd64.zip \
 && unzip terraform_0.12.29_linux_amd64.zip \
 && mv terraform /usr/local/bin/ \
 && rm terraform_0.12.29_linux_amd64.zip

RUN pip install protobuf grpcio cryptography u-msgpack-python requests

ADD Pyrraform/src /Pyrraform
RUN cd /Pyrraform && pip install .

ADD terraform-provider-freebox/src /terraform-provider-freebox
RUN cd /terraform-provider-freebox && pip install .
