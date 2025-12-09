FROM docker.io/python:3.11-slim AS base
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1

FROM base AS builder
RUN pip install pipenv
COPY Pipfile* ./
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base
RUN adduser --uid 65532 nonroot
COPY --from=builder /.venv /.venv
ENV PATH="/.venv/bin:$PATH"
COPY *.py LICENSE ./

EXPOSE 8080 9090
USER 65532
ENV prometheus_multiproc_dir=/tmp
ENTRYPOINT ["/.venv/bin/gunicorn", "-c", "gunicorn_conf.py", "server:app"]
