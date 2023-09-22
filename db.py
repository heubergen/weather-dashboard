#!/usr/bin/env python3

from sqlite3 import connect as sqlconnect
connection = None
def create_connection():
	global connection
	if connection == None:
		try:
			connection = sqlconnect("data.sqlite")
			print("Connected")
		except:
			raise ConnectionError()
		
	return connection

if __name__ == '__main__':
	create_connection()