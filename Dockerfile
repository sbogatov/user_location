FROM python:3.11.4-slim

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./
COPY . $WORKDIR

RUN poetry install

EXPOSE 8000
