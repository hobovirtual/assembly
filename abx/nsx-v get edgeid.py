import requests
import pybase64
from xml.etree import ElementTree as ET

def handler(context, inputs):
    print('action started')
    
    # encode credentials to base64
    stringtoencode = inputs["username"]+':'+inputs["password"]
    encodedcreds = pybase64.b64encode(stringtoencode.encode("utf-8"))
    creds = str(encodedcreds, "utf-8")
    print("encoded credentials: "+creds)
    
    # define authorization
    auth = "Basic "+creds
    
    # define headers
    headers = {"Accept": "application/xml", "Content-Type": "application/xml", "Authorization": auth}
    
    # disable proxy for internal api request
    proxies = {
      "http": None,
      "https": None,
    }
    
    # initiate request
    response = requests.get(inputs["url"]+"/api/4.0/edges",headers=headers, proxies=proxies, verify=False)
    
    # parse xml
    xmlparse = ET.fromstring(response.content)
    for edge in xmlparse[0].findall('edgeSummary'):
        edgeid = edge.find('objectId').text
        if edgeid == inputs["edgeidtosearch"]:
            print('nsx '+edgeid+' found')
            return edgeid

    # display various response information
    #print("requests status code: "+str(response.status_code))
    #print("requests content: "+str(response.content))
    #print("requests headers: "+str(response.headers))