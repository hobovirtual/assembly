import requests
import json
    
def handler(context, inputs):
  #replace uri parameter(s)
  uri = inputs['uri'].replace("[deploymentid]",inputs["deploymentId"])
  
  # define headers
  headers = {"Content-Type": "application/json", "Authorization": "Bearer "+inputs['token']}
  
  #get available resource actions
  response = requests.get(uri, headers = headers, verify = False)
  
  #define array of resourceid(s)
  outputs = {}
  arraydict = []

  if response.status_code == 200:
    jsonresponse = response.json().get('content')
    for obj in jsonresponse:
      jsondump = json.dumps(obj)
      jsoncontent = json.loads(jsondump)
      if jsoncontent.get('type') == "Cloud.vSphere.Machine":
        arraydict.append(jsoncontent.get('id'))
        
  outputs['resourceids'] = arraydict
  return outputs