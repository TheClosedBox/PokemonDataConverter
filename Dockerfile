# syntax=docker/dockerfile:1
FROM python:3.9-alpine3.15

WORKDIR /app
COPY . .
RUN pip install --disable-pip-version-check -q -r requirements.txt
CMD [ "python", "-u", "populate.py" ]