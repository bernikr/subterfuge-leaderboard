#!/bin/sh

git remote set-url origin https://github.com/bernikr/subterfuge-leaderboard.git
git fetch
git reset --hard origin/master

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

printenv | sed 's/^\(.*\)$/export \1/g' > /root/project_env.sh
chmod u+x /root/project_env.sh

cp /usr/src/cronjobs /etc/cron.d/cjob
chmod 0644 /etc/cron.d/cjob
touch /var/log/cron.log

cron
gunicorn leaderboard.wsgi:application --bind 0.0.0.0:8000
