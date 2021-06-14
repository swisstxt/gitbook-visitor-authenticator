FROM python:3.8-slim
RUN pip install --no-cache-dir pipenv
WORKDIR /app
COPY Pipfile* /app/
COPY config.yaml /app/
RUN cd /app && \
    pipenv install --system --deploy
# Maybe "pipenv sync" would be better. I'm unsure:
# https://pipenv-fork.readthedocs.io/en/latest/advanced.html#using-pipenv-for-deployments
COPY * /app/
EXPOSE 8080 9090
ENV prometheus_multiproc_dir=/tmp
CMD ["gunicorn", "-c", "gunicorn_conf.py", "server:app"]
