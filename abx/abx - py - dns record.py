# default inputs
#   powershell-user = secret with powershell host username
#   powershell-password = secret with powershell host username password
#
# dependency
#   pywinrm
# 
import winrm
import socket

#global variables
event = ""
ipaddress = ""
vmname = ""

def get_deployment_informations(context, inputs):
    global event
    global ipaddress
    global vmname
    
    event = str(inputs["__metadata"]["eventTopicId"])
    ipaddress = str(inputs["addresses"][0][0])
    vmname = str(inputs["resourceNames"][0])
    
def pwsh_status (pwsh):
    port = 5986
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((pwsh, int(port)))
        conn.shutdown(2)
        return True
    except:
        return False

def handler(context, inputs):
    #function variables
    user = context.getSecret(inputs["powershell-user"])
    password = context.getSecret(inputs["powershell-password"])
    zone = "domain.local"
    pwshhosts = ["host1.domain.local","host2.domain.local"]
    
    get_deployment_informations(context, inputs)
    
    #define powershell script command / inputs based on event
    if str(event).startswith('compute.provision'):
        script = 'D:\\library\\powershell\\cm-create-dns.ps1 -zone '+zone+' -name '+vmname+' -ip '+ipaddress
        
    if str(event).startswith('compute.removal'):
        script = 'D:\\library\\powershell\\cm-delete-dns.ps1 -zone '+zone+' -name '+vmname+' -ip '+ipaddress

    #validate powershell host pwsh_status
    for pwshhost in pwshhosts:
        pwshstate = pwsh_status(pwshhost)
        if pwshstate == True:
            session = winrm.Session(pwshhost, auth=(user, password),transport='ntlm',server_cert_validation='ignore')
            result = session.run_ps(script)
            print(result.std_out.decode('utf-8'))
            print(result.status_code)
            
            #break loop if successful
            if (result.status_code == 0):
                break