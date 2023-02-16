# Jazzwares_Facepad

Take home test for Jazzwares.

## Requirements

You will need docker and docker-compose installed  
Please see documentation for how to install these on your local machine

- [Docker Install] (https://docs.docker.com/engine/install/)
- [Docker-Compose Install] (https://docs.docker.com/compose/install/)

## Usage

1. Clone the repository and cd into the root directory of the project
2. Make an .env.dev file with the following environment variables set only change the values that have the // Can change this value comment:
   DEBUG=1
   SECRET_KEY=foo // Can change this value
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1] // Can change this value
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE=facepad_dev // Can change this value
   SQL_USER=facepad_user // Can change this value
   SQL_PASSWORD=facepad_password //Can change this value
   SQL_HOST=db //Can change this value
   SQL_PORT=5432
   DATABASE=postgres
3. Once there run the following code
   `docker-compose up -d --build`
4. This should get the system running once running you should create a super user
5. To create a super user do the following from the command line:
   - `docker exec -it jazzwares-facepad_web_1 sh`
   - `python3 manage.py createsuperuser`
   - follow the prompts and you will have a super user created

## Notes

This is a dev copy of the app not at all production ready
