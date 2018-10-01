# Docker
```
docker run -d --restart=always --name=cronjobs -v /home/cronjob:/cronjob cronjob:0.1
```
```
docker run -d --restart=always --name=cronjobs -v /home/cronjob:/cronjob -v /home/periodic:/etc/periodic cronjob:0.1
```


