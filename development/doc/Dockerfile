FROM python:3.8

RUN pip install \
      sphinx

ENTRYPOINT ["/entrypoint.sh"]

COPY development/doc/entrypoint.sh /
RUN chmod +x /entrypoint.sh
