FROM registry.gitlab.com/kimvanwyk/python3-poetry-container:latest

COPY ./secretish_balloting/ /app/
COPY run.sh /app

VOLUME /storage

ENV STORAGE_DIR=/storage

ENTRYPOINT ["bash", "run.sh"]
