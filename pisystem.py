#!/usr/bin/env python3

import logging
from sqlite3 import connect as sqlconnect, Error as sqlerror
from subprocess import check_output as sub_check_output

# connect to database
def create_connection(path):
	connection = None
	try:
		connection = sqlconnect(path)
	except sqlerror as e:
		print(f"The error '{e}' occurred")
		
	return connection

connection = create_connection("data.sqlite")

# logging settings
logging.basicConfig(
	filename='/var/log/pisystem-exporter.log',
	encoding='utf-8',
	level=logging.INFO,
	format='%(asctime)s %(levelname)-8s %(message)s')

def pisystem_read_data():
	pitempf = round(int(sub_check_output('cat /sys/class/thermal/thermal_zone0/temp', shell=True, text=True)) / 1000, 2)
	piload = float(sub_check_output('cut -f 1 -d " " /proc/loadavg', shell=True, text=True))
	pimemory = round(int(sub_check_output("cat /proc/meminfo | grep MemFree | awk '{ print $2 }'", shell=True, text=True)) / 1024, 2)
	pilines = [pitempf,piload,pimemory]
	try:
		for piline in pilines:
			sqlcount += 1
			connection.execute('UPDATE pisystem_data SET Value =\"' + str(piline) + '\" WHERE ID = ' + str(sqlcount) + ';')
		connection.commit()
	except:
		logging.error('There was an issue when writing to the database', exc_info=True)
		raise ConnectionError()
	finally:
		connection.close()
		
	logging.debug('Database writing successful, ending program')
	
	logging.debug('End of program reached')

if __name__ == '__main__':
	pisystem_read_data()