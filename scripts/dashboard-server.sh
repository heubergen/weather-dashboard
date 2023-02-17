#!/usr/bin/env bash
set -Eeuo pipefail

wfilename="/opt/meteo-exporter/data.txt"
wcounter=0
while read wline; do
	wlines[wcounter]="$wline"
	wcounter=$((wcounter+1))
done < $wfilename

ifilename="/opt/co2-exporter/data.txt"
icounter=0
while read iline; do
	ilines[icounter]="$iline"
	icounter=$((icounter+1))
done < $ifilename

pitempf=$(sudo /usr/bin/vcgencmd measure_temp | awk -F "[=']" '{print($2 * 1.8)+32}')
piload=$(cut -f 1 -d " " /proc/loadavg)
pimemory=$(awk '/MemFree/ { printf "%.0f \n", $2/1024 }' /proc/meminfo | sed 's/ *$//')

dates=('YYYY-MM-DD' 'YYYY-MM-DD' 'YYYY-MM-DD')
now=$(date +'%Y-%m-%d')
count=0

if [[ $OSTYPE == 'darwin'* ]]; then
	for date in "${dates[@]}"; do
		diff=$((`date -jf %Y-%m-%d $date +%s` - `date -jf %Y-%m-%d $now +%s`))
		days[count]="$(($diff/ 86400))"
		weeks[count]="$(($diff/ 604800))"
		count=$(( $count + 1 ))
	done
elif [[ $OSTYPE == 'linux'* ]]; then
	for date in "${dates[@]}"; do
		let diff=(`date +%s -d $date`-`date +%s -d $now`)
		days[count]="$(($diff/ 86400))"
		weeks[count]="$(($diff/ 604800))"
		count=$(( $count + 1 ))
	done
else
	echo "OS not supported, please patch script"
fi

touch /var/www/html/index.html

cat > /var/www/html/index.html <<- EOF
# Copy content from www/index.html
EOF
exit
