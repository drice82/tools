# Docker

```
docker run -d --restart=always --name=cronjobs -v /home/cron/cronjob:/cronjob -v /home/cron/periodic:/etc/periodic drice64/tools:cronjob
```
cronjob:
scripts exec able
periodic:
15min/hourly/daily/weekly/monthly/


