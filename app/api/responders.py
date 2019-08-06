import json
from app_api import app

def api_respond(dataframe):
    return app.response_class(
        response=json.dumps(dataframe.to_dict()),
        status=200,
        mimetype='application/json'
    )
