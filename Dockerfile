FROM python:3.14.0-alpine3.22

RUN apk add --no-cache sqlite

RUN addgroup -S 2000 && adduser -S 2000 -G 2000
COPY src /src
WORKDIR /src

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

USER 2000:2000

ARG APP_VERSION="alpha"
ENV APP_VERSION=$APP_VERSION

ENTRYPOINT ["python", "main.py"]
