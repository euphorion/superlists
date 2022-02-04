New site work support:
=======================
## Required packages:
* nginx
* python 3.9
* virtualenv + pip
* Git

E.g. in Ubuntu:
	sudo apt-repository ppa:fkrull/deadsnakes
	sudo apt-get install nginx git python39 python3.9-venv

## Configuring Nginx node:

* Check nginx.template.conf
* Replace SITENAME with e.g. staging.my-domain.com

## Folder structure:
If user has a record in /home/username
/home/username
/home/albotret
└── sites
    └── 185.247.118.195
        ├── database
        ├── source
        ├── static
        └── virtualenv

