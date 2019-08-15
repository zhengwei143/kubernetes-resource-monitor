import json
import requests
import pandas as pd
from app_api import app
from flask import request
from redis_store import *
from .responders import *
from dataframes.filters import apply_params_filter

def log_request(path, params):
    app.logger.debug('Received request {} with params {}'.format(path, params))

@app.route('/pods', methods=['GET'])
def get_pods():
    log_request('/pods', request.args)
    pod_key = get_key('pod')
    pods_dataframe = retrieve_dataframe(pod_key)
    result = apply_params_filter(pods_dataframe, params=request.args)
    return api_respond(result)

@app.route('/nodes', methods=['GET'])
def get_nodes():
    log_request('/nodes', request.args)
    pod_key = get_key('node')
    pods_dataframe = retrieve_dataframe(pod_key)
    result = apply_params_filter(pods_dataframe, params=request.args)
    return api_respond(result)

@app.route('/services', methods=['GET'])
def get_services():
    log_request('/services', request.args)
    pod_key = get_key('service')
    pods_dataframe = retrieve_dataframe(pod_key)
    result = apply_params_filter(pods_dataframe, params=request.args)
    return api_respond(result)

@app.route('/ingress', methods=['GET'])
def get_ingress():
    log_request('/ingress', request.args)
    pod_key = get_key('ingress')
    pods_dataframe = retrieve_dataframe(pod_key)
    result = apply_params_filter(pods_dataframe, params=request.args)
    return api_respond(result)

@app.route('/pvcs', methods=['GET'])
def get_pvcs():
    log_request('/pvcs', request.args)
    pod_key = get_key('pvc')
    pods_dataframe = retrieve_dataframe(pod_key)
    result = apply_params_filter(pods_dataframe, params=request.args)
    return api_respond(result)

@app.route('/deployments', methods=['GET'])
def get_deployments():
    log_request('/deployments', request.args)
    pod_key = get_key('deployment')
    pods_dataframe = retrieve_dataframe(pod_key)
    result = apply_params_filter(pods_dataframe, params=request.args)
    return api_respond(result)
