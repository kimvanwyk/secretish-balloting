FROM registry.gitlab.com/kimvanwyk/python3-poetry-container:latest

COPY ./secretish_balloting/ /app/

VOLUME /storage

ENV STORAGE_DIR=/storage

ENTRYPOINT ["gunicorn", "secretish_balloting.wsgi:application", "--bind", "0.0.0.0:8000"]
