# catalystapp

## Installation instructions

### Docker Installation(tested on ubuntu 17.10)
Install docker for your platform using the [link](https://docs.docker.com/install/)

### Bring up the docker instances
Source the setenv file

``` bash
	cd server 
	source setenv
```

if docker-compose is not installed, install it using pip

``` bash
	sudo apt-get install python-pip # if pip isn't installed
	pip install docker-compose
```

Start docker instances using

``` bash
	docker-compose build
	docker-compose up      # use -d flag to run it in daemon mode
```

### Notes

- Docker-compose exposes port 8000 so you can connect to the web browser using localhost:8000
- check the logs in daemon mode using docker-compose logs -f easykrishi_server

Create support tickets in case something doesn't work


