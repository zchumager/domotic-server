### create or modify domotic-server service
sudo nano /etc/systemd/system/domotic-dev.service

### check domotic-server service status
> sudo systemctl status domotic-dev

### enable domotic-server service
> sudo systemctl enable domotic-dev

### start domotic-server service
> sudo systemctl start domotic-dev

### stop domotic-server service
> sudo systemctl stop domotic-dev

### Run when domotic-server service file is modified
> sudo systemctl daemon-reload