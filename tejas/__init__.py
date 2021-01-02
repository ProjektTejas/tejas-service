import os
import sys

from celery.apps.worker import Worker
from loguru import logger

from tejas.core.config import settings
from tejas.core.celery_app import celery_app

config = {"handlers": [{"sink": sys.stdout, "format": settings.LOGURU_FORMAT}]}

logger.configure(**config)

if "TEJAS_LAMBDA" in os.environ:
    import sys
    from celery import current_app

    sys.path.insert(0, os.environ["TEJAS_LIBS_PATH"])

    from mangum import Mangum
    from .main import app

    # for sockets
    # handler = Mangum(app, dsn="dynamodb://tejassockets?region=ap-south-1")
    # for just http
    handler = Mangum(app)

    worker: Worker = celery_app.Worker()

    worker.start()
