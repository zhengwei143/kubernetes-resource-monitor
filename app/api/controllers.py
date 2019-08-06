import json
import requests
import pandas as pd
from app_api import app
from flask import request
from redis_store import *
from dataframes.filters import apply_params_filter

@app.route('/pods', methods=['GET'])
def get_pods():
    pod_key = get_key('pod')
    pods_dataframe = retrieve_dataframe(pod_key)
    result = apply_params_filter(pods_dataframe, params=request.args)
    print(result)
    # print("Data: ", request.args)
    # pods_dict = pods_dataframe.to_dict()
    # d = pd.DataFrame(pods_dict)
    # result = apply_params_filter(pods_dataframe, params=request.args)

    # print(pods_json)
    return app.response_class(
        response=json.dumps({ "data": "hello~!"}),
        status=200,
        mimetype='application/json'
    )
