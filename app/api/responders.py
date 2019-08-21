import json
from app_api import app

def api_respond(objects):
    return app.response_class(
        response=json.dumps(objects),
        status=200,
        mimetype='application/json'
    )
