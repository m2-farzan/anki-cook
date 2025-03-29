FROM python:3.12-slim

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_INSTALLER_PARALLEL=false
ENV POETRY_HOME=/opt/poetry

ADD https://install.python-poetry.org /tmp/get-poetry.py
RUN python /tmp/get-poetry.py --version 2.1.1
ENV PATH="${POETRY_HOME}/bin:${PATH}"

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --without dev --no-root

COPY ./ ./

RUN poetry install --no-interaction --without dev

EXPOSE 8000
ENTRYPOINT [ "poetry", "run", "gunicorn", "anki_cook.server.app:app" ]
