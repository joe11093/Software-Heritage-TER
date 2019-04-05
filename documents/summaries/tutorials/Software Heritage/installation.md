# Installation of Software Heritage in develop mode
## Pre-requisites
1. **installation of mr (myrepos)** : `sudo apt install myrepos`
1. **installation of docker and docker-compose** : *(cf. docker_summary.pdf)*
1. **installation of other dependencies** :
    - `sudo wget https://www.postgresql.org/media/keys/ACCC4CF8.asc -O /etc/apt/trusted.gpg.d/postgresql.asc`
    - `sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'`
    - `sudo apt update`
    - `sudo apt install python3 python3-venv libsvn-dev postgresql-11 libsystemd-dev libpython3-dev graphviz postgresql-autodoc postgresql-server-dev-all virtualenvwrapper git build-essential`
1. **installing the virtualenvwrapper using pip**: `pip3 install virtualenvwrapper`
1. **locating the virtualenvwrapper shell script** : `which virtualenvwrapper.sh (usually /usr/local/bin/virtualenvwrapper.sh)`
1. in the **.bashrc file** :
    - creating an **environment variable** that will contain the path to all **virtual environments** created by **mkvirtualenv** : `export WORKON_HOME=`(directory you need to save envs)
    - **executing the virtualenvwrapper shell script** to be able to use the **mkvirtualenv command** : `source /usr/local/bin/virtualenvwrapper.sh -p $WORKON_HOME`

## Installation of SWH
1. **checking out the source code** : `git clone https://forge.softwareheritage.org/source/swh-environment.git && cd swh-environment`
2. **checking out the swh packages source repositories** : `bin/update`
