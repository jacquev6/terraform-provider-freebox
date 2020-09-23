FROM python:3.8

RUN pip install \
      sphinx

ENTRYPOINT ["/entrypoint.sh"]

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
