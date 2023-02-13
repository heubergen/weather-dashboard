#!/usr/bin/env bash
set -Eeuo pipefail

wfilename="/opt/meteo-exporter/data.txt"
wcounter=0
while read wline; do
	wlines[wcounter]="$wline"
	#echo "wlines[$wcounter] = ${wlines[wcounter]}"
	wcounter=$((wcounter+1))
done < $wfilename

ifilename="/opt/co2-exporter/data.txt"
icounter=0
while read iline; do
	ilines[icounter]="$iline"
	#echo "ilines[$icounter] = ${ilines[icounter]}"
	icounter=$((icounter+1))
done < $ifilename

pitempf=$(sudo /usr/bin/vcgencmd measure_temp | awk -F "[=']" '{print($2 * 1.8)+32}')
piload=$(cut -f 1 -d " " /proc/loadavg)
pimemory=$(awk '/MemFree/ { printf "%.0f \n", $2/1024 }' /proc/meminfo | sed 's/ *$//')

touch /var/www/html/index.html

cat > /var/www/html/index.html <<- EOF
<!DOCTYPE html>
<html lang="en-US">
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta charset="UTF-8">
				<link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgo=">
	<title>
		Weather Dashboard
	</title>
	<link rel="stylesheet" href="css/mystyle.css">
	<script defer src="js/countdown.js"></script>
</head>
<body>
	<h1>
		Indoor
	</h1>
	<div class="group">
		<label for="intemp">Current temperatur:</label> <meter id="intemp" min="59" max="100" low="66" high="77" optimum="72" value="${ilines[1]}"></meter>
		<p class="infotext">
			${ilines[1]}
		</p>
	</div>
	<div class="group">
		<label for="co2">Current carbon dioxide level:</label> <meter id="co2" min="0" max="3000" low="400" high="1000" optimum="400" value="${ilines[0]}"></meter>
		<p class="infotext">
			${ilines[0]}
		</p>
	</div>
	<div class="group">
		<label for="inahum">Current relative air humidity:</label> <meter id="inahum" min="0" max="100" low="45" high="60" optimum="50" value="${ilines[2]}"></meter>
		<p class="infotext">
			${ilines[2]}
		</p>
	</div>
	<h1>
		Outdoor
	</h1>
	<div class="group">
		<label for="temp">Current temperatur:</label> <meter id="temp" min="0" max="120" low="41" high="86" optimum="20" value="${wlines[0]}"></meter>
		<p class="infotext">
			${wlines[0]}
		</p>
	</div>
	<div class="group">
		<label for="prec">Current precipitation:</label> <meter id="prec" min="0" max="1.17" low="0" high="0.039" optimum="0.0195" value="${wlines[1]}"></meter>
		<p class="infotext">
			${wlines[1]}
		</p>
	</div>
	<div class="group">
		<label for="ahum">Current relative air humidity:</label> <meter id="ahum" min="0" max="100" low="45" high="60" optimum="50" value="${wlines[2]}"></meter>
		<p class="infotext">
			${wlines[2]}
		</p>
	</div>
	<div class="group">
		<label for="wind">Current wind speed:</label> <meter id="wind" min="0" max="155" low="0" high="19" optimum="0" value="${wlines[3]}"></meter>
		<p class="infotext">
			${wlines[3]}
		</p>
	</div>
	<div class="group">
		<label for="apre">Current air pressure:</label> <meter id="apre" min="23" max="45" low="28" high="36" optimum="29.5" value="${wlines[4]}"></meter>
		<p class="infotext">
			${wlines[4]}
		</p>
	</div>
	<h1> DietPi </h1>
	<div class="group">
			<label for="temp">Current temperatur:</label> <meter id="pitemp" min="60" max="180" low="77" high="104" optimum="86" value="${pitempf}"></meter>
			<p class="infotext">
					${pitempf}
			</p>
	</div>
	<div class="group">
			<label for="temp">Current load:</label> <meter id="piload" min="0" max="2" low="0" high="0.5" optimum="0.2" value="${piload}"></meter>
			<p class="infotext">
					${piload}
			</p>
	</div>
	<div class="group">
			<label for="temp">Current free memory:</label> <meter id="pimemory" min="0" max="450" low="200" high="400" optimum="385" value="${pimemory}"></meter>
			<p class="infotext">
					${pimemory}
			</p>
	</div>
	<h1>
		Countdowns
	</h1>
	<div class="group">
		<label for="event1">Event 1</label> <p id="event1" data-time="2023-09-01" class="countdown"></p>
		<p class="infotext">
		</p>
	</div>
	<div class="group">
		<label for="event2">Event 2</label> <p id="event2" data-time="2025-09-01" class="countdown"></p>
		<p class="infotext">
		</p>
	</div>
	<div class="group">
		<label for="event3">Event 3</label> <p id="event3" data-time="2027-04-01" class="countdown"></p>
		<p class="infotext">
		</p>
	</div>
</body>
</html>
EOF
sleep 900
exit
