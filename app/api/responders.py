import json
from app_api import app

def api_respond(objects_list):
    return app.response_class(
        response=json.dumps({ 'items': objects_list }),
        status=200,
        mimetype='application/json'
    )
