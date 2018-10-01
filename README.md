# Docker
```
docker run -d --restart=always --name=cronjobs -v /home/cronjob:/cronjob cronjob:latest
```
```
docker run -d --restart=always --name=cronjobs -v /home/cron/cronjob:/cronjob -v /home/cron/periodic:/etc/periodic cronjob:latest
```


