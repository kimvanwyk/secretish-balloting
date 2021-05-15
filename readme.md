# Secretish Balloting

A [Python](https://www.python.org/) [Django](https://www.djangoproject.com/) app to permit secretish balloting for somewhat anonymised users (not completely secret nor anonymous as the app owner can see the database).

# Usage

The app can control one or more ballots as required. 

## Setup and Administration

Administration is all done via the admin dashboard, at the /admin endpoint. Login details are set as environment variables, as per the [Deployment](#deployment) section.

## Voters

Voters for each ballot are sent an email containing a unique URL (which includes an 8 digit randomly created numerical value) at which they can cast their vote. Voters can cast their vote more than once but only the most recent vote is recorded.

## Observers

A unique URL (which includes an 8 digit randomly created numerical value) is generated for each ballot which shows the current results of the ballot.

# Deployment

Some environment variables need to be set - see the **.env.example** file for details. The [dotenv](https://pypi.org/project/python-dotenv/) module is included so a *.env* file can be placed in the root directory with the necessary environment variables.

The project is setup to use a sqlite database. This can however be modified in the Django settings as desired.

## Docker

The app is built into a Docker container, which may be the easiest way to deploy it. See [this Gitlab container registry](https://gitlab.com/kimvanwyk/secretish-balloting/container_registry).

# Documentation

Read The Docs documentation is being written - this readme will be updated to point to it when it is available.

# Development and Contributions

This project was developed over the course of a a few weeks to meet a specific need and could certainly be improved in many ways.

I consider myself a competent Python developer but there are always new things to learn and practices to improve on. In particular I am in no way a Django or testing expert. I welcome contributions as pull requests, issues or comments.

# Authors
    
- [Kim van Wyk](https://kimvanwyk.co.za/)

# License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) license.

  
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
![Gitlab Build](https://img.shields.io/gitlab/pipeline/kimvanwyk/secretish-balloting/master)

  

  


  
