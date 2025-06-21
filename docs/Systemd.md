### Copy file from systemd/domotic-server.service into /etc/systemd/system
> sudo cp ./systemd/domotic-server.service /etc/systemd/system

### check domotic-server service status
> sudo systemctl status domotic-server.service

### enable domotic-server service
> sudo systemctl enable domotic-server.service

### start domotic-server service
> sudo systemctl start domotic-server.service

### stop domotic-server service for
> sudo systemctl stop domotic-server.service

### Run when domotic-server service file is modified
> sudo systemctl daemon-reload

### Edit domotic-server service if needed
> sudo nano /etc/systemd/system/domotic-server.service

Note: service need to be stopped for file's modification
