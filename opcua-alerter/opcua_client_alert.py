import asyncio
import sys
import os
import logging
import logging
import logging.handlers
import logging_loki
from datetime import datetime
from asyncua import Client, Node, ua
from trycourier import Courier

mailer = Courier(auth_token="YOURTOKEN")

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

opc_ua_client_logger = logging.getLogger('OPC UA Client Handler')
opc_ua_client_logger.setLevel(logging.WARNING)
handler = logging_loki.LokiHandler(
    url="http://loki-stack.loki-stack:3100/loki/api/v1/push", 
    #url="http://localhost:3100/loki/api/v1/push", #run kubectl port-forward --namespace loki-stack service/loki-stack 3100:3100 on the side
    tags={"application": "OPC-UA_Pump_Sensors"},
    version="1",
)
opc_ua_client_logger.addHandler(handler)


def mailsend(url, timecode):
    opc_ua_client_logger.critical('sending alert email now')
    resp = mailer.send_message(
        message={
            "to": {
                "email": "YOURMAIL"
            },
            "content": {
                "title": "Alert from your k3s cluster!",
                "body": "Hello from k3s ! A pump detected by akri at url {{url}} have reported a BROKEN status !"
            },
                "data":{
                "url": url
            }
        }
    )


async def main():
    #uncomment those to get logs when pod start up
    #opc_ua_client_logger.critical('pod starting with env var : %s', os.environ)
    #_logger.info(os.environ)

    #switch comment on those if you want to run it locally
    url = os.environ.get('OPCUA_DISCOVERY_URL')
    #url = 'opc.tcp://192.168.236.3:4840/'

    async with Client(url=url) as client:
        uri = 'http://devnetiot.com/opcua/'
        idx = await client.get_namespace_index(uri)
        status = await client.nodes.root.get_child(["0:Objects", f"{idx}:vPLC1", f"{idx}:pumpstatus"])
        timestamp = await client.nodes.root.get_child(["0:Objects", f"{idx}:vPLC1", f"{idx}:timestamp"])
        while True:
            statusvalue = await status.read_value()
            timestampvalue = await timestamp.read_value()
            if statusvalue == "BROKEN":
                opc_ua_client_logger.critical('pump is reporting a BROKEN state at %s', datetime.now())
                mailsend(url, datetime.now())
                #print("BROKEN MACHINE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #print("Pump status", status, statusvalue, " at timestamp ", timestamp, timestampvalue)
            await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
