Script permettant de récupérer par l'interface fibre optique de la livebox 6 pour la domotique par exemple:

- IP V4
- IP V6
- UPTIME
- STATUS de l'interface Fibre
- La température de la BOX

Commande:

$ python livebox6_getapi.py  -l
dict_keys(['IPV4_WAN', 'IPV6_WAN', 'UPTIME', 'INTERFACE_WAN_STATUS', 'BOX_TEMP'])

$ python livebox6_getapi.py  -k IPV4_WAN
X.X.X.X

$ python livebox6_getapi.py  -k IPV6_WAN
fexx::xxxx:xxxx:xxxx:xxxx

$ python livebox6_getapi.py  -k UPTIME
9 days, 13:22:54sec 

$ python livebox6_getapi.py  -k INTERFACE_WAN_STATUS
up

$ python livebox6_getapi.py  -k BOX_TEMP
50°




---------------------------------------



Script to retrieve through the fiber interface of the livebox 6 for home automation for example:

- IP V4
- IP V6
- UPTIME
- STATUS of the fibre interface
- The temperature of the BOX

Command:

$ python livebox6_getapi.py -l
dict_keys(['IPV4_WAN', 'IPV6_WAN', 'UPTIME', 'INTERFACE_WAN_STATUS', 'BOX_TEMP'])


$ python livebox6_getapi.py -k IPV4_WAN
X.X.X.X

$ python livebox6_getapi.py -k IPV6_WAN
fexx::xxxx:xxxx:xxxx:xxxx

$ python livebox6_getapi.py  -k UPTIME
9 days, 13:22:54sec 

python livebox6_getapi.py -k INTERFACE_WAN_STATUS
up

$ python livebox6_getapi.py -k BOX_TEMP
50°

