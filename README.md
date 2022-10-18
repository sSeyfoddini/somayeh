# Pocket Strata

## Intro

This application is a simple, lightweight "thin client" which acts as a secure intermediary between ASU’s real SIS systems and Pocket’s application servers. It securely connects ASU SIS databse resources to Pocket Strata via a RESTFUL API service, protecting PII and SIS access credentials while still enabling Pocket engineers to work with a realistic interface and realistically structured data.

This thin-client is developed by the Pocket engineering team, but deployed and run by ASU engineers. The thin client performs the following functions:

* Provides an API interface for direct-to-DB connections.
* Proxies requests between Pocket’s servers and the ASU SIS system.
* Securely and irrevocably anonymizes ALL data on the fly before it is passed to Pocket.
  * Non-PII data can be exempted from scrubbing by including the field name in the `data_scrubbing_whitelist.yaml` file.
* Holds SIS DB access-credentials “at arms length” from the Pocket team.

The following Endpoints are available:

* /v1/health/health
  * GET, no arguments.
  * Returns confirmation of service health and successful DB connection.
* /v1/student/students
  * GET, JSON body `{"email_set": ["example1@example1.com", "example2@example2.com"]}`
  * Returns one or more student objects.

## Docs

To run this project locally, you will need to install:

* Python 3.8

It also necessary to create and and fill out an `.env` file. This should be copied from the `.env-example` file.

---------
To run with pipenv:
```
pip install pipenv
pipenv install
pipenv shell
flask run
```

---------
- To create database tables run:
```
 flask db upgrade
 ```

 ---------
 - To get data from data broker and populate the Strata tables:
```
 flask credential_type
 flask colleges
 flask academic
 flask organization
 flask role
 flask term
 flask general
 flask program
 flask course
 ```

---------
To run with docker:
```
docker build -t thin-client .
docker run --env-file .env -e ENV='LOCAL' -d -p 5000:5000 thin-client
```

---------
Swagger address:
```
{Base_Url}strata/v1/doc
```

 ## Database Migration
  ```
 flask db migrate -m "Initial migration."
  ```