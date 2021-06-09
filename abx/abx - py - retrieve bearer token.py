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
  headers = {"Content-Type": "application/x-www-form-urlencoded"}
   
  # define request body
  payload = {'refresh_token':context.getSecret(inputs["vra-refreshtoken"])}
 
  # login request
  response = requests.post(inputs['uri'], headers = headers, data = payload, verify = False)
 
  # extract bearer token
  if response.status_code == 200:
    token = response.json().get('access_token')
   
    if token:
      outputs = {}
      outputs['token'] = token
      return outputs
    else:
      raise Exception("could not retrieve token from content response, please validate: ",token)
     
  else:
    print(response.text)
    raise Exception("error returned from rest operation: ",response.status_code)
