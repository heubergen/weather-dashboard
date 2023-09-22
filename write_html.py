from db import Database

Database().connection

def write_html(cname):
	local_weather_html = ''
	local_weather_html += '<h1>' + cname.capitalize() + '</h1><div class="' + cname + '">'
	rows = connection.execute("SELECT * from " + cname + "_data")
	for row in rows:
		count =+ 1
		local_weather_html += '<div class="group">'
		local_weather_html += '<label for="' + cname + '-' + str(count) + '">' + row[1] + ':</label> <meter id="' + cname + '-' + str(count) + '" min="' + str(row[3]) + '" max="' + str(row[4]) + '" low="' + str(row[5]) + '" high="' + str(row[6]) + '" optimum="' + str(row[7]) + '" value="' + str(row[2]) + '"></meter>'
		local_weather_html += '<p class="infotext">' + str(row[2]) + '</p></div>'
	local_weather_html += '</div>'
	return local_weather_html

def write_sections():
	weather_html = ''
	weather_html += write_html('indoor')
	weather_html += write_html('weather')
	weather_html += write_html('pisystem')
	return weather_html

if __name__ == '__main__':
	write_sections()