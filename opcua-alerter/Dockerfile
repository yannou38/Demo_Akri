FROM python:3.9
RUN pip3 install python-logging-loki trycourier asyncua==0.8.4
COPY opcua_client_alert.py opcua_client_alert.py


CMD [ "python", "./opcua_client_alert.py" ]
