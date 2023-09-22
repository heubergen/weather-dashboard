#!/usr/bin/env python3

from base64 import decode
from io import StringIO
from urllib.request import urlopen
from csv import DictReader
import logging
from db import create_connection


# connect to database
connection = create_connection()

# set settings, you usually only need to modify the next two variables
loc = 'KLO' # the location you want to read the data out, download https://data.geo.admin.ch/ch.meteoschweiz.messnetz-automatisch/ch.meteoschweiz.messnetz-automatisch_en.csv and add the Abbreviation here

# change variables here only if the location changes or the structure
download = 'https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/VQHA80.csv'
temp = 'tre200s0' # the column name where the temperature can be found
prec = 'rre150z0' # the column name where the precipitation can be found
humi = 'ure200s0' # the column name where the relative air humidity can be found
wspe = 'fu3010z0' # the column name where the wind speed can be found
press = 'prestas0' # the column name where the air pressure can be found
# logging settings
logging.basicConfig(
	filename='/Users/patrickalbrecht/weather-dashboard-gitmeteo-exporter.log',
	encoding='utf-8',
	level=logging.INFO,
	format='%(asctime)s %(levelname)-8s %(message)s')

def weather_read_data():
	sqlcount = 0
	logging.debug('Start program')
	logging.debug('Downloading data')
	try:
		data = urlopen(download).read().decode('UTF-8')
		dataFile = StringIO(data)
		csvReader = DictReader(dataFile, delimiter=';')
	except:
		logging.error('There was an issue with the download', exc_info=True)
		raise ConnectionError()
	else:
		logging.debug('Download successful, continue with data processing')
		for row in csvReader:
			if row['Station/Location'] == loc:
				tempp = float(row.get(temp))
				precp = float(row.get(prec))
				humip = float(row.get(humi))
				wspep = float(row.get(wspe))
				pressp = float(row.get(press))
				break
		dewpo = round((tempp - ((100 - humip)/5)),2)
		lines = [tempp,precp,humip,dewpo,wspep,pressp]
		logging.debug('Data processing successful, writing data into database')
		try:
			for line in lines:
				sqlcount += 1
				connection.execute('UPDATE weather_data SET Value =\"' + str(line) + '\" WHERE ID = ' + str(sqlcount) + ';')
			connection.commit()
		except:
			logging.error('There was an issue when writing to the database', exc_info=True)
			raise ConnectionError()
			
		logging.debug('Database writing successful, ending program')
		
	finally:
		logging.debug('End of program reached')

if __name__ == '__main__':
	weather_read_data()