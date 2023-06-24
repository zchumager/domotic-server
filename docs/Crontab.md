### Run python cronjob script as sudo for single execution with venv
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python cronjob.py

### obtain python interpreter path
> which python

### open cron table on terminal
> crontab -e

### Add cron expression
'* * * * * /home/admin/Repos/domotic-server/venv/bin/python /home/admin/Repos/domotic-server/cronjob.py'