# default inputs
#   uri = https://{vra}/iaas/login
#   vra-refreshtoken = secret with token value (currently manually refreshed every 90 days)
# 
# dependency
#   requests
# 
import requests
import json

def handler(context, inputs):
  # define headers
  headers = {"Content-Type": "application/json"}
    
  # define request body
  body = {}
  body['refreshToken'] = context.getSecret(inputs["vra-refreshtoken"])
    
  # login request
  response = requests.post(inputs['uri'], headers = headers, data = json.dumps(body), verify = False)
    
  # extract bearer token
  if response.status_code == 200:
    token = response.json().get('token')
    outputs = {}
    outputs['token'] = token
    return outputs