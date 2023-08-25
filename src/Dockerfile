FROM python:3.11-slim-buster AS base

ENV PYTHONFAULTHANDLER=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=10000

RUN apt-get -y update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

RUN mkdir -p /home/url_shortener/src
RUN addgroup --system app && adduser --system --group app
RUN chown -R app:app /home/url_shortener/src
USER app
WORKDIR /home/url_shortener/src

FROM base AS dependencies_stage

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

FROM dependencies_stage

COPY . .
