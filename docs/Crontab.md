### Run python cronjob script as sudo for single execution with venv
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python cronjob.py

### obtain python interpreter path
> which python

### open cron table on terminal
> sudo crontab -e

### Add cron expression on crontab to execute cronjob.py every 2 minutes
*/2 * * * * /home/admin/Repos/domotic-server/venv/bin/python /home/admin/Repos/domotic-server/cronjob.py

Note: There is no need to reboot Raspberry Pi

# Verify cron service status is active (running)
> sudo systemctl status cron


