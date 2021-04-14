### Base ###
FROM python:3.7.10-alpine3.13 AS base

RUN apk add --no-cache git

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY requirements/base.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .



### Dev ###
FROM nikolaik/python-nodejs:python3.7-nodejs14-alpine AS dev

RUN yarn global add nodemon

ENV PATH="/opt/venv/bin:$PATH"

COPY --from=base /opt/venv /opt/venv
COPY --from=base /app /app

WORKDIR /app

CMD nodemon --exec "python" server.py



### Prod ###
FROM python:3.7.10-alpine3.13 AS prod

ENV PATH="/opt/venv/bin:$PATH"

COPY --from=base /opt/venv /opt/venv
COPY --from=base /app /app

WORKDIR /app

CMD python /app/server.py


