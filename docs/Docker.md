update package manager
> sudo apt-get update

install certificates
> sudo apt-get install ca-certificates curl gnupg

download docker script with curl
> curl -fsSL https://get.docker.com -o shellscripts/get-docker.sh

install docker
> sudo shellscripts/get.docker.sh

download homeassistant docker's image
> sudo docker pull homeassistant/home-assistant

check docker compose installation
> docker compose version

run container as daemon with docker compose
> sudo docker compose up -d