import pandas as pd
from redis_store import *
from flask import Flask

app = Flask(__name__)

from api.controllers import *

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8003, debug=True)
