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
logging.basicConfig(
        filename='/var/log/co2-exporter.log',
        encoding='utf-8',
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s')

if __name__ == '__main__':
        logging.info('Start program')
        logging.debug('Accessing metrics from sensor')
        try:
                CO2 = round(scd.CO2, 2)
                temperature = scd.temperature
                relative_humidity = round(scd.relative_humidity, 2)
                lines = [CO2,temperature,relative_humidity]
        except:
                logging.error('Accessing metrics failed')
        else:
                lines[1] = round((temperature * 1.8) + 32,2)
                logging.debug('Accessing metrics successful, continue with data processing')
                logging.debug('Writing data into file')
                with open('/opt/co2-exporter/data.txt', 'w') as f:
                        print('\n'.join(str(line) for line in lines),file=f)
        finally:
                logging.debug('End program')
