FROM python:2.7.15-alpine

WORKDIR /cf_ddns

COPY /root /
RUN apk add --no-cache tzdata \
  && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
  && pip install --no-cache-dir -r requirements.txt \
  && echo "*/5 * * * *  python /cf_ddns/cloudflare_ddns.py /cf_ddns/config.yaml" >> /etc/crontabs/root \
  && rm -rf /var/cache/apk/*
CMD ["/usr/sbin/crond","-c","/etc/crontabs","-f"]
