FROM python:3.11-slim as python-base

ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m venv $VIRTUAL_ENV \
    && pip install --upgrade pip wheel setuptools

FROM python-base as builder

WORKDIR /src

COPY pyproject.toml .
COPY src /src/src

RUN pip install --no-cache-dir .

FROM python-base

WORKDIR /src

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

COPY alembic.ini /src
COPY src /src/src

CMD ["uvicorn", "--factory", "app.main.app:get_app", "--host", "0.0.0.0", "--port", "8000"]