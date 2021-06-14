FROM python:3.8-slim

RUN useradd -d /app -m appuser
USER appuser

WORKDIR /app

COPY Pipfile* /app/
COPY *.py /app/
COPY LICENSE /app/

RUN pip install --no-cache-dir pipenv
RUN /app/.local/bin/pipenv install --system --deploy
# Maybe "pipenv sync" would be better. I'm unsure:
# https://pipenv-fork.readthedocs.io/en/latest/advanced.html#using-pipenv-for-deployments

EXPOSE 8080 9090
ENV prometheus_multiproc_dir=/tmp
CMD ["/app/.local/bin/gunicorn", "-c", "gunicorn_conf.py", "server:app"]
