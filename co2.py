#!/usr/bin/env python3

import logging
import board
import busio
import adafruit_scd30
from db import create_connection


# connect to database
connection = create_connection()

# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
i2c = busio.I2C(board.SCL, board.SDA,frequency=50000)
scd = adafruit_scd30.SCD30(i2c)

scd.temperature_offset = 2 #change if needed

# logging settings
logging.basicConfig(
	filename='/var/log/co2-exporter.log',
	encoding='utf-8',
	level=logging.INFO,
	format='%(asctime)s %(levelname)-8s %(message)s')

def co2_read_data():
	sqlcount = 0
	logging.debug('Start program')
	logging.debug('Accessing metrics from sensor')
	try:
		temperature = round(scd.temperature)
		CO2 = round(scd.CO2, 2)
		relative_humidity = round(scd.relative_humidity, 2)
		lines = [temperature,CO2,relative_humidity]
	except:
		logging.error('Accessing metrics failed', exc_info=True)
		raise ValueError()
	else:
		logging.debug('Accessing metrics successful, continue with data processing')
		try:
			for line in lines:
				sqlcount += 1
				connection.execute('UPDATE indoor_data SET Value =\"' + str(line) + '\" WHERE ID = ' + str(sqlcount) + ';')
			connection.commit()	
		except:
			logging.error('There was an issue when writing to the database', exc_info=True)
			raise ConnectionError()
			
		logging.debug('Database writing successful, ending program')
			
	finally:
		logging.debug('End of program reached')

if __name__ == '__main__':
	co2_read_data()