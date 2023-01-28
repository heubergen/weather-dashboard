from base64 import decode
from io import StringIO
import urllib.request
import csv
import time
import logging

# set settings, you usually only need to modify the next two variables
loc = 'ENTER_ABBREVIATION' # the location you want to read the data out, download https://data.geo.admin.ch/ch.meteoschweiz.messnetz-automatisch/ch.meteoschweiz.messnetz-automatisch_en.csv and add the Abbreviation here

# change variables here only if the location changes or the structure
download = 'https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/VQHA80.csv'
temp = 'tre200s0' # the column name where the temperature can be found
prec = 'rre150z0' # the column name where the precipitation can be found
humi = 'ure200s0' # the column name where the relative air humidity can be found
wspe = 'fu3010z0' # the column name where the wind speed can be found
press = 'prestas0' # the column name where the air pressure can be found
# logging settings
logging.basicConfig(
    filename='/var/log/meteo-exporter.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s')

if __name__ == '__main__':
    logging.info('Start program')
    while True:
        logging.debug('Downloading data')
        try:
            data = urllib.request.urlopen(download).read().decode('UTF-8')
            dataFile = StringIO(data)
            csvReader = csv.DictReader(dataFile, delimiter=';')
        except:
            logging.error('Downloading file failed, please check connection and download variable')
        else:
            logging.debug('Download successful, continue with data processing')
            for row in csvReader:
                if row['Station/Location'] == loc:
                    tempp = row.get(temp)
                    precp = row.get(prec)
                    humip = row.get(humi)
                    wspep = row.get(wspe)
                    pressp = row.get(press)
                    break
            lines = [tempp,precp,humip,wspep,pressp]
            logging.debug('Writing data into file')
            with open('/opt/meteo-exporter/data.txt', 'w') as f:
                for line in lines:
                    f.write(line)
                    f.write('\n')
        finally:
            logging.debug('Sleep until next data processing starts')
            time.sleep(900)
