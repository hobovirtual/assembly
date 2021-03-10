# default inputs
#   uri = https://{vra}/deployment/api/deployments/[deploymentid]/resources/[resourceid]/requests
#   uritask = https://{vra}/deployment/api/requests/[taskid]
# 
import requests
import json
import time

#---
#this function will define the requested information for adding a cloud volume - day2 resources
def definerequestbody(id, size, inputs):
  #define request input
  requestinputs = {}
  requestinputs['name'] = 'disk'
  requestinputs['capacityGb'] = size
  requestinputs['encrypted'] = False
  requestinputs['persistent'] = False
  requestinputs['constraints'] = 'env:'+str(inputs["requestInputs"]["environment"])

  #request body
  body = {}
  body['actionId'] = inputs['actionid']
  body['inputs'] = requestinputs
  return body

#---
#this function will return the status of a given request
def checkrequeststatus(headers, taskid, inputs):
  #replace uri parameter(s)
  uri = inputs['uritask'].replace("[taskid]",taskid)
  
  #retrieve task request status
  response = requests.get(uri, headers = headers, verify = False)
     
  #response output to json
  jsoncontent = response.json()
  
  #retrieve task id
  taskstatus = jsoncontent.get('status')
  return taskstatus

#---
#main function
def handler(context, inputs):
  arrdisks = inputs["requestInputs"]["disks"]
  
  for resourceid in inputs["resourceids"]:
      #replace uri parameter(s)
      uri = inputs['uri'].replace("[deploymentid]",inputs["deploymentid"])
      uri = uri.replace("[resourceid]",resourceid)
      
      #define headers
      headers = {"Content-Type": "application/json", "Authorization": "Bearer "+inputs['token']}
    
      for disk in arrdisks:
        size = disk['size']
        taskstatus = ""
        
        #function which will define the request body
        body = definerequestbody(id, size, inputs)
        
        #post add disk resource action
        response = requests.post(uri, headers = headers, data = json.dumps(body), verify = False)
        print("adding disk ...")
        
        #response output to json
        jsoncontent = response.json()
        
        #task id
        taskid = jsoncontent.get('id')
        
        if response.status_code == 200:
          #request validation loop - validation is performed for a maximum of 120 seconds
          for i in range(20):
            taskstatus = checkrequeststatus(headers, taskid, inputs)
            if taskstatus == "SUCCESSFUL":
              print("disk "+str(id)+" added successfully")
              break
          
            elif taskstatus == "FAILED":
              print("disk "+str(id)+" addition task returned an error, please validate the deployment history for more details")
              print("status: "+taskstatus)
              break
          
            time.sleep(6)
        
        else:
          print("api call return error: "+str(response.status_code))
          print("error message: "+response.reason)
          raise Exception("error occured during the action request, please validate return code and body content")