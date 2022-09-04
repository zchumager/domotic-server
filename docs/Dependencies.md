### Verify Python Installation
> python --version

### Create venv
> python -m venv venv

### Activate venv for linux
> source ./venv/bin/activate

### Activate venv for Windows
> .\venv\Scripts\activate

### Upgrade pip, setuptools
>  python -m pip install --upgrade pip setuptools

### Backup dependencies
> python -m pip freeze > requirements.txt

### Install dependencies
python -m pip install -r ./requirements.txt
