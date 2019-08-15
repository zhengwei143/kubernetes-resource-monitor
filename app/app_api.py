import pandas as pd
import logging
from redis_store import *
from flask import Flask

app = Flask(__name__)
gunicorn_debug_logger = logging.getLogger('gunicorn.debug')
app.debug = True
app.logger.handlers.extend(gunicorn_debug_logger.handlers)
app.logger.setLevel(logging.DEBUG)

from api.controllers import *

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8003, debug=True)
