FROM python:2.7.15-alpine

WORKDIR /cf_ddns

COPY /root /
RUN pip install --no-cache-dir -r requirements.txt

CMD crond && python /cf_ddns/cloudflare_ddns.py /cf_ddns/config.yaml
