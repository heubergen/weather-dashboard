# weather-dashboard
A set of python and bash scripts that collect data from your room with a co2 sensor and outside from the Swiss Meteo service to display them in a simple dashboard.

## Prerequisites
You need to have the following services installed and ready:
* A webserver that checks /var/www/html
* python3 and pip3

Also make sure that your co2 sensor is ready to use.

## Installation
Only steps for Debian are provided, for other distros or OS they might differ.
1. `mkdir /opt/co2-exporter /opt/meteo-exporter /opt/weather-dashboard`
3. `cp scripts/co2-server.py /opt/co2-exporter/server.py`
4. `cp scripts/meteo-server.py /opt/meteo-exporter/server.py`
5. `cp scripts/dashboard-server.sh /opt/weather-dashboard/server.sh`
6. `cp service-config/* /etc/systemd/system/`
7. `systemctl daemon-reload`
5. `sudo systemctl enable co2-exporter meteo-exporter weather-dashboard`
6. `pip3 install adafruit-circuitpython-scd30`
7. `sudo systemctl start co2-exporter meteo-exporter weather-dashboard`