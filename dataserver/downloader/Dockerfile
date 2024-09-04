FROM alpine

RUN which crond && rm -rf /etc/periodic
RUN apk --no-cache add curl

COPY crontab /var/spool/cron/crontabs/root

CMD ["crond", "-f", "-l", "2"]
