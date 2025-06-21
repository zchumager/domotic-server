It is required to create config folder for Home Assistant container storage before running docker container

Create config folder inside container directory for docker compose configuration
> mkdir /home/admin/Repos/domotic-server/container/config

Start Home Assistant using docker-compose.yml
> sudo docker compose up -d