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
# Copy content from www/index.html
EOF
exit
