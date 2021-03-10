# default inputs
#   uri = https://{vra}/deployment/api/deployments/[deploymentid]/resources/[resourceid]/actions
#
# dependency
#   requests
# 
import requests
import json

def handler(context, inputs):
  #replace uri parameter(s)
  uri = inputs['uri'].replace("[deploymentid]",inputs["deploymentId"])
  uri = uri.replace("[resourceid]",inputs["resourceids"][0])
  
  # define headers
  headers = {"Content-Type": "application/json", "Authorization": "Bearer "+inputs['token']}
  
  #get available resource actions
  response = requests.get(uri, headers = headers, verify = False)
  
  if response.status_code == 200:
    jsonresponse = response.json()
    for obj in jsonresponse:
      jsondump = json.dumps(obj)
      jsoncontent = json.loads(jsondump)
      if str(jsoncontent.get('name')) == "Add.Disk" and str(jsoncontent.get('valid') == "true"):
        outputs = {}
        outputs['actionid'] = str(jsoncontent.get('id'))
        outputs['deploymentid'] = inputs["deploymentId"]
        return outputs