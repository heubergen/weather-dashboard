#!/usr/bin/env python3

from sqlite3 import connect as sqlconnect, Error as sqlerror
from re import sub
from datetime import date
from datetime import datetime
from math import floor
from time import time
from subprocess import check_output as sub_check_output
from weather import weather_read_data
from co2 import co2_read_data
from pisystem import pisystem_read_data

weather_read_data()
co2_read_data()
pisystem_read_data()

def create_connection(path):
	connection = None
	try:
		connection = sqlconnect(path)
	except sqlerror as e:
		print(f"The error '{e}' occurred")
		
	return connection

connection = create_connection("data.sqlite")
NOW = date.today()
BIRTH = date(1996, 4, 1)

weather_html = '<body><h1>Indoor</h1><div class="indoor">'

irows = connection.execute("SELECT * from indoor_data")
icount = 0
for irow in irows:
	icount =+ 1
	weather_html += '<div class="group">'
	weather_html += '<label for="indoor-' + str(icount) + '">' + irow[1] + ':</label> <meter id="indoor-' + str(icount) + '" min="' + str(irow[3]) + '" max="' + str(irow[4]) + '" low="' + str(irow[5]) + '" high="' + str(irow[6]) + '" optimum="' + str(irow[7]) + '" value="' + str(irow[2]) + '"></meter>'
	weather_html += '<p class="infotext">' + str(irow[2]) + '</p></div>'
	
weather_html += '</div>'

weather_html += '<h1>Outdoor</h1><div class="outdoor">'

wrows = connection.execute("SELECT * from weather_data")
wcount = 0
for wrow in wrows:
	wcount += 1
	weather_html += '<div class="group">'
	weather_html += '<label for="outdoor-' + str(wcount) + '">' + wrow[1] + ':</label> <meter id="outdoor-' + str(wcount) + '" min="' + str(wrow[3]) + '" max="' + str(wrow[4]) + '" low="' + str(wrow[5]) + '" high="' + str(wrow[6]) + '" optimum="' + str(wrow[7]) + '" value="' + str(wrow[2]) + '"></meter>'
	weather_html += '<p class="infotext">' + str(wrow[2]) + '</p></div>'
	
weather_html += '</div>'

weather_html += '<h1>DietPi</h1><div class="dietpi">'

pirows = connection.execute("SELECT * from pisystem_data")
for pirow in pirows:
	pcount =+ 1
	weather_html += '<div class="group">'
	weather_html += '<label for="pisystem-' + str(pcount) + '">' + pirow[1] + ':</label> <meter id="pisystem-' + str(pcount) + '" min="' + str(pirow[3]) + '" max="' + str(pirow[4]) + '" low="' + str(pirow[5]) + '" high="' + str(pirow[6]) + '" optimum="' + str(pirow[7]) + '" value="' + str(pirow[2]) + '"></meter>'
	weather_html += '<p class="infotext">' + str(pirow[2]) + '</p></div>'
	
weather_html += '</div>'

weather_html += '</div>'

with open('header.html', 'r') as file:
	html_header = file.read()

with open('footer.html', 'r') as file:
	html_footer = file.read()
	
countdown_html = '<h1>Countdowns</h1><div class="countdowns">'
crows = connection.execute("SELECT * from countdowns")
for crow in crows:
	ndiffr = datetime.strptime(crow[2], '%Y-%m-%d').date() - NOW
	ndiffd = ndiffr.days
	ndiffw = round(ndiffd/7,1)
	bdiffr = datetime.strptime(crow[2], '%Y-%m-%d').date() - BIRTH
	bdiffd = bdiffr.days
	bdiffy = floor(bdiffd / 365.2425)
	countdown_html += '<div class="group">'
	countdown_html += '<label for="' + str(crow[0]) + '">' + crow[1] + '</label> <p id="' + str(crow[0]) + '" class="countdown"> ' + str(ndiffd) + ' days / ' + str(ndiffw) + ' weeks / ' + str(bdiffy) + ' years old</p>'
	countdown_html += '</div>'
	
html_code = (html_header + weather_html + countdown_html + html_footer)
html_minimized = sub('<!--(.*?)-->|\s\B', '', html_code)
with open('index_new.html', 'w') as f:
	f.writelines(html_code)
connection.close()