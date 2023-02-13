# weather-dashboard
A set of python and bash scripts that collect data from your room with a co2 sensor and outside from the Swiss Meteo service to display them in a simple dashboard.
Some js countdowns are also included.

## Prerequisites
You need to have the following services installed and ready:
* A webserver that checks /var/www/html
* python3 and pip3

Also make sure that your SCD-30 sensor is ready to use.

## Installation
Only steps for Debian are provided, for other distros or OS they might differ.
1. `mkdir /opt/co2-exporter /opt/meteo-exporter /opt/weather-dashboard`
2. `mkdir /var/www/html/css /var/www/html/js`
3. `cp www/css/mystyle.css /var/www/html/css/`
4. `cp www/js/countdown.css /var/www/html/js/`
5. `cp scripts/co2-server.py /opt/co2-exporter/server.py`
6. `cp scripts/meteo-server.py /opt/meteo-exporter/server.py`
7. `cp scripts/dashboard-server.sh /opt/weather-dashboard/server.sh`
8. Add `*/15 * * * * python3 /opt/co2-exporter/server.py ; python3 /opt/meteo-exporter/server.py ; bash /opt/weather-dashboard/server.sh` to as a cron

The service file were used in the past, but here the steps to use them. You will need to add a while loop and sleep to prevent the scripts from exiting.

1. `cp service-config/* /etc/systemd/system/`
2. `systemctl daemon-reload`
3. `sudo systemctl enable co2-exporter meteo-exporter weather-dashboard`
4. `sudo systemctl start co2-exporter meteo-exporter weather-dashboard`