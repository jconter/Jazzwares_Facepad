# Jazzwares_Facepad

Take home test for Jasswares.

## Requirements

You will need docker and docker-compose installed  
Please see documentation for how to install these on your local machine

- [Docker Install] (https://docs.docker.com/engine/install/)
- [Docker-Compose Install] (https://docs.docker.com/compose/install/)

## Usage

1. Clone the repository and cd into the root folder
2. Once there run the following code
   `docker-compose up -d --build`
3. This should get the system running once running you should create a super user
4. To create a super user do the following from the command line:
   - `docker exec -it jazzwares-facepad_web_1 sh`
   - `python3 manage.py createsuperuser`
   - follow the prompts and you will have a super user created
