#!/usr/bin/env bash
set -Eeuo pipefail

wfilename="/opt/meteo-exporter/data.txt"
wcounter=0
while read -r wline; do
	wlines[wcounter]="$wline"
	wcounter=$((wcounter+1))
done < $wfilename

ifilename="/opt/co2-exporter/data.txt"
icounter=0
while read -r iline; do
	ilines[icounter]="$iline"
	icounter=$((icounter+1))
done < $ifilename

pitempf=$(sudo /usr/bin/vcgencmd measure_temp | awk -F "[=']" '{print($2 * 1.8)+32}')
piload=$(cut -f 1 -d " " /proc/loadavg)
pimemory=$(awk '/MemFree/ { printf "%.0f \n", $2/1024 }' /proc/meminfo | sed 's/ *$//')

dates=('YYYY-MM-DD' 'YYYY-MM-DD' 'YYYY-MM-DD')
now=$(date +'%Y-%m-%d')
birth='YYYY-MM-DD'
count=0

command_not_installed () {
	echo "Please install $1 and make sure it's included in your PATH"
	exit
}

set_dates () {
	days[count]="$diff"
	if [ "$1" = true ] ; then
		birthd[count]=$((diffbirth / 365))
	fi
	weekstmp=$(echo "$diff"/ 7 | bc -l)
	weeks[count]=$(printf "%.1f" "$weekstmp")
}

if command -v bc &> /dev/null; then
	:
else
	command_not_installed bc
fi

if command -v datediff &> /dev/null; then
	datediffcommand="datediff"
elif command -v dateutils.ddiff &> /dev/null ; then
	datediffcommand="dateutils.ddiff"
else
	command_not_installed dateutils
fi
for date in "${dates[@]}"; do
	diff=$("$datediffcommand" "$now" "$date")
	diffbirth=$("$datediffcommand" "$birth" "$date")
	set_dates true
	count=$(( count + 1 ))
done

diff=$("$datediffcommand" "$now" "$birth")
set_dates false

touch /var/www/html/index.html

cat > /var/www/html/index.html <<- EOF
# Copy content from www/index.html
EOF
exit
