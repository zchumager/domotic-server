Install pyenv dependencies
> sudo apt install libbz2-dev -y
> sudo apt install libedit-dev -y
> sudo apt-get install libffi-dev -y
> sudo apt install zlib1g zlib1g-dev -y
> sudo apt install libssl-dev libsqlite3-dev -y
> sudo apt install libreadline-dev -y
> sudo apt install liblzma-dev -y
> sudo apt install tk-dev -y

Install pyenv: https://github.com/pyenv/pyenv
> curl https://pyenv.run | bash

Install python 3.9.6 with pyenv
> pyenv install 3.9.6

Set python 3.9.6
> pyenv global 3.9.6

Install nmap with apt
> sudo apt install nmap -y

Scan network with nmap
> sudo nmap -snP <raspberry.pi.ip.address>/24

Create venv on domotic server root folder
> python -m venv venv

Activate venv from domotic server root folder
>  source ./venv/bin/activate

Update pip
> python -m pip install --upgrade pip

Install requirements.txt with venv 
> python -m pip install -r requirements.txt
