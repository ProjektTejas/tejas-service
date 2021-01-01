import os
import sys

from loguru import logger

from tejas.core.config import settings

config = {"handlers": [{"sink": sys.stdout, "format": settings.LOGURU_FORMAT}]}

logger.configure(**config)

if "TEJAS_LAMBDA" in os.environ:
    import sys

    sys.path.insert(0, os.environ["TEJAS_LIBS_PATH"])

    from mangum import Mangum
    from .main import app

    # for sockets
    # handler = Mangum(app, dsn="dynamodb://tejassockets?region=ap-south-1")
    # for just http
    handler = Mangum(app)
