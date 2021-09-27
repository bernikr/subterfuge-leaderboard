#!/bin/sh

mkdir ~/.ssh
ssh-keyscan github.com >> ~/.ssh/known_hosts
git pull https://github.com/bernikr/subterfuge-leaderboard.git master

pip install -r requirements.txt

python manage.py collectstatic
python manage.py migrate

printenv | sed 's/^\(.*\)$/export \1/g' > /root/project_env.sh
chmod u+x /root/project_env.sh

cp /usr/src/cronjobs /etc/cron.d/cjob
chmod 0644 /etc/cron.d/cjob
touch /var/log/cron.log

cron
gunicorn leaderboard.wsgi:application --bind 0.0.0.0:8000
