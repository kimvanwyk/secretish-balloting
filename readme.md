# Introduction

A [Python](https://www.python.org/) [Django](https://www.djangoproject.com/) app to permit secretish balloting for somewhat anonymised users (not completely secret nor anonymous as the app owner can see the database).

# Usage

Some environment variables need to be set - see the **.env.example** file for details. The [dotenv](https://pypi.org/project/python-dotenv/) module is included so a *.env* file can be placed in the root directory with the necessary environment variables.

The project is setup to use a sqlite database. This can however be modified in the Django settings as desired.

## Docker

The app is built into a Docker container, which may be the easiest way to deploy it. See [this Gitlab container registry](https://gitlab.com/kimvanwyk/secretish-balloting/container_registry).

## Documentation

Read The Docs documentation is being written - this readme will be updated to point to it when it is available.
