#!/usr/bin/env python3

from db import create_connection
from re import sub
from datetime import date
from datetime import datetime
from math import floor
from weather import weather_read_data
from co2 import co2_read_data
from pisystem import pisystem_read_data
from write_html import write_sections

weather_read_data()
co2_read_data()
pisystem_read_data()

connection = create_connection()
NOW = date.today()
BIRTH = date(1996, 4, 1)

weather_html = write_sections()

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
with open('/var/www/html/index.html', 'w') as f:
	f.writelines(html_code)
connection.close()