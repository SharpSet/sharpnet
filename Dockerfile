FROM docker:29.9.2-cli AS dockercli
FROM python:3.13-slim-trixie
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends nginx ca-certificates && rm -rf /var/lib/apt/lists/*
RUN sed -i -e 's|^mozilla/emSign_ECC_Root_CA_-_G3.crt|!&|' -e 's|^mozilla/Comodo_AAA_Services_root.crt|!&|' /etc/ca-certificates.conf && update-ca-certificates
COPY --from=dockercli /usr/local/bin/docker /usr/local/bin/docker
ENV PIP_CERT=/etc/ssl/certs/ca-certificates.crt
RUN pip install --no-cache-dir --upgrade 'pip>=26.2.2'
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
RUN mkdir -p /etc/nginx/test.d /usr/share/nginx/html && rm -f /etc/nginx/sites-enabled/default
RUN python3 -m pip uninstall -y pip && rm -rf /usr/local/lib/python*/ensurepip/_bundled/*
COPY ./sharpnet /sharpnet/
ENTRYPOINT ["python3"]
CMD ["-um", "sharpnet"]
