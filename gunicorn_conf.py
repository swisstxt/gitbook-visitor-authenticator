import logging
import multiprocessing

import gunicorn.glogging
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

# Create custom /healthz request filter for Logger
class HealthzFilter(logging.Filter):
    def filter(self, record):
        return "/healthz" not in record.getMessage()
class Logger(gunicorn.glogging.Logger):
    def setup(self, cfg):
        super().setup(cfg)
        logger = logging.getLogger("gunicorn.access")
        logger.addFilter(HealthzFilter())

# Called just after the server is started.
def when_ready(server):
    GunicornPrometheusMetrics.start_http_server_when_ready(9090)

# Called just after a worker has been exited, in the master process.
def child_exit(server, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)

# Gunicorn config variables
logger_class = Logger
loglevel = "info"
workers = multiprocessing.cpu_count()
bind = "0.0.0.0:8080"
keepalive = 120
accesslog = "-"
errorlog = "-"
