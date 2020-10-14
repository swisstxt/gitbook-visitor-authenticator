FROM python:3.8-slim
RUN pip install --no-cache-dir pipenv
COPY . /app
WORKDIR /app
RUN cd /app && \
    pipenv install --system --deploy
# Maybe "pipenv sync" would be better. I'm unsure:
# https://pipenv-fork.readthedocs.io/en/latest/advanced.html#using-pipenv-for-deployments
CMD ["waitress-serve", "server:app"]
