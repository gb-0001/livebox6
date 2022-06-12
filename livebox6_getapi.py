#!/usr/bin/python
#GB-0001 github
import json
import requests
from dictor import dictor
## Converting seconds to days, hours, minutes and seconds in Python
import datetime, time
import os
import argparse
import sys

###>
#Keyword List argument -k
    # IPV4_WAN
    # IPV6_WAN
    # UPTIME
    # INTERFACE_WAN_STATUS
    # BOX_TEMP


# Script permettant de récupérer par l'interface fibre optique de la livebox 6 pour la domotique par exemple:

# - IP V4
# - IP V6
# - UPTIME
# - STATUS de l'interface Fibre
# - La température de la BOX

# Commande:

# $ python livebox6_getapi.py  -l
# dict_keys(['IPV4_WAN', 'IPV6_WAN', 'UPTIME', 'INTERFACE_WAN_STATUS', 'BOX_TEMP'])

# $ python livebox6_getapi.py  -k IPV4_WAN
# X.X.X.X

# $ python livebox6_getapi.py  -k IPV6_WAN
# fexx::xxxx:xxxx:xxxx:xxxx

# $ python livebox6_getapi.py  -k UPTIME
# 9 days, 13:22:54sec 

# $ python livebox6_getapi.py  -k INTERFACE_WAN_STATUS
# up

# $ python livebox6_getapi.py  -k BOX_TEMP
# 50°

###>

local_box_ip="192.168.1.1"
local_box_id="admin"
#Environment Variable
local_box_pw=os.environ.get('KPSSBX')


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--password", required=False, type=str,
help="Define password")
ap.add_argument("-l", "--keywordlist", action="store_true",
help="Keyword list")
ap.add_argument("-k", "--keyword", required=False, type=str,
help="Define keyword")
ap.add_argument("-v", "--verbose", action="store_true",
help="Verbose")
args = vars(ap.parse_args())

def verbosemod(data):
    if args["verbose"]:
        print(data)

def getapi(dicapiout,dicchoicekey,keyword):
    if keyword in dicchoicekey:
        getvalue=dictor(dicapiout, str(dicchoicekey[keyword][0]) )
        if dicchoicekey[keyword][1]:
            if keyword == "UPTIME":
                getvalue = str(datetime.timedelta(seconds = (dictor(dicapiout, dicchoicekey[keyword][0]))))
            getvalue = str(getvalue) + str(dicchoicekey[keyword][1])
        return getvalue
    else:
        print("Keyword doesn't exist")
        sys.exit(1)


dicchoice = {
    'IPV4_WAN': ('status.dhcp.dhcp_data.IPAddress',''),
    'IPV6_WAN': ('status.netdev.bridge_gvmulti.IPv6Addr.dyn5.Address',''),
    'UPTIME': ('status.dhcp.dhcp_data.Uptime','sec '),
    'INTERFACE_WAN_STATUS': ('status.netdev.bridge_gvmulti.NetDevState',''),
    'BOX_TEMP': ('status.gpon.veip0.Temperature','°')

}

if args["keywordlist"]:
    print(dicchoice.keys())
    sys.exit(0)

if not local_box_pw:
    if not args["password"]:
        print("Define password")
        sys.exit(1)


# Authentication
url = "http://" + local_box_ip + "/ws"
headers = {'Content-Type': 'application/x-sah-ws-4-call+json',
'Authorization': 'X-Sah-Login'}
datas = "{\"service\":\"sah.Device.Information\",\"method\":\"createContext\",\"parameters\":{\"applicationName\":\"so_sdkut\",\"username\":\"" + local_box_id + "\",\"password\":\"" + local_box_pw + "\"} }"

r = requests.post(url,headers=headers, data=datas)
dicapioutput=json.loads(r.content)


#Get Context ID
specific_key='contextID'

found=False
def contextIDreturn(dico):
    for element in dico.values():
        if isinstance(element, dict):
            for k, v in element.items():
                #print(k,' ',v)
                if k.startswith(specific_key):
                    found=True
                    #print("BINGO:",k,v)
                    return v
            if found:
                break 


#Get cookie
cookie=r.cookies.items()
cookie=dict((x, y) for x, y in cookie)

#Data
headers = '''{"Content-Type": "application/x-sah-ws-4-call+json", "X-Context": "''' +  contextIDreturn(dicapioutput) + '''"}'''
headers=json.loads(headers)
datas1 = "{\"service\":\"NeMo.Intf.data\",\"method\":\"getMIBs\",\"parameters\":{}}"
MIBs = requests.post(url,headers=headers, data=datas1,cookies=cookie)
MIBs = json.loads(MIBs.text)


verb=json.dumps(MIBs, indent=4, sort_keys=True)
verbosemod(verb)

output = getapi(MIBs,dicchoice,str(args["keyword"]))

print(output)
