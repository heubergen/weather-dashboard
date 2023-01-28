#!/usr/bin/env bash
set -Eeuo pipefail

while true
do
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

        touch /var/www/html/index.html

        cat > /var/www/html/index.html <<- EOF
        <!DOCTYPE html>
        <html lang="en-US">
                <head>
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <meta charset="UTF-8">
                        <title>
                                Weather Dasboard
                        </title>
                        <link rel="stylesheet" href="css/mystyle.css">
		</head>
		<body>
			<h1>
				Indoor
			</h1>
			<div class="group">
				<label for="intemp">Current temperatur:</label> <meter id="intemp" min="20" max="40" low="19" high="25" optimum="22" value="${ilines[1]}"></meter>
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
				<label for="temp">Current temperatur:</label> <meter id="temp" min="-25" max="45" low="5" high="30" optimum="20" value="${wlines[0]}"></meter>
				<p class="infotext">
					${wlines[0]}
				</p>
			</div>
			<div class="group">
				<label for="prec">Current precipitation:</label> <meter id="prec" min="0" max="30" low="0" high="1" optimum="0.5" value="${wlines[1]}"></meter>
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
				<label for="wind">Current wind speed:</label> <meter id="wind" min="0" max="250" low="0" high="30" optimum="0" value="${wlines[3]}"></meter>
				<p class="infotext">
					${wlines[3]}
				</p>
			</div>
			<div class="group">
				<label for="apre">Current air pressure:</label> <meter id="apre" min="800" max="1500" low="950" high="1200" optimum="1000" value="${wlines[4]}"></meter>
				<p class="infotext">
					${wlines[4]}
				</p>
			</div>
		</body>
	</html>
	EOF
	sleep 900
done
