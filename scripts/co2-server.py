import time
import logging
import board
import busio
import adafruit_scd30

# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
i2c = busio.I2C(board.SCL, board.SDA,frequency=50000)
scd = adafruit_scd30.SCD30(i2c)

scd.temperature_offset = 2 #change if needed

# logging settings
logging.basicConfig(filename='/var/log/co2-exporter.log', encoding='utf-8', level=logging.DEBUG)

if __name__ == '__main__':
    logging.info('Start program')
    while True:
        logging.debug('Accessing metrics from sensor')
        try:
            CO2_str = str(round(scd.CO2, 2))
            temperature_str = str(round(scd.temperature, 2))
            relative_humidity_str = str(round(scd.relative_humidity, 2))
            lines = [CO2_str,temperature_str,relative_humidity_str]
        except:
            logging.error('Accessing metrics failed')
        else:
            logging.debug('Accessing metrics successful, continue with data processing')
            logging.debug('Writing data into file')
            with open('/opt/co2-exporter/data.txt', 'w') as f:
                for line in lines:
                    f.write(line)
                    f.write('\n')
        finally:
            logging.debug('Sleep until next data processing starts')
            time.sleep(900)
