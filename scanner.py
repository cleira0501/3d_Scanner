#      ******************************************************************
#      *                                                                *
#      *                                                                *
#      *    Example Python program that receives data from an Arduino   *
#      *                                                                *
#      *                                                                *
#      ******************************************************************


import serial
import csv
import datetime

#
# Note 1: This python script was designed to run with Python 3.
#
# Note 2: The script uses "pyserial" which must be installed.  If you have
#         previously installed the "serial" package, it must be uninstalled
#         first.
#
# Note 3: While this script is running you can not re-program the Arduino.
#         Before downloading a new Arduino sketch, you must exit this
#         script first.
#

#
# Set the name of the serial port.  Determine the name as follows:
#	1) From Arduino's "Tools" menu, select "Port"
#	2) It will show you which Port is used to connect to the Arduino
#
# For Windows computers, the name is formatted like: "COM6"
# For Apple computers, the name is formatted like: "/dev/tty.usbmodemfa141"
#
arduinoComPort = "/dev/cu.usbmodem101"
data = []

#
# Set the baud rate
# NOTE1: The baudRate for the sending and receiving programs must be the same!
# NOTE2: For faster communication, set the baudRate to 115200 below
#        and check that the arduino sketch you are using is updated as well.
#
baudRate = 9600

dataFile = f'./data/{datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")}.csv'
# dataFile = f'./calibration/60.csv'


#
# open the serial port
#
serialPort = serial.Serial(arduinoComPort, baudRate, timeout=1)

def getDistance(x):
  # 117 + -0.362x + 3.4E-04x^2
  return (117 - 0.362*x + (3.4e-4 * x**2))

#
# main loop to read data from the Arduino, then display it
#
while True:
  #
  # ask for a line of data from the serial port, the ".decode()" converts the
  # data from an "array of bytes", to a string
  #
  lineOfData = serialPort.readline().decode()

  #
  # check if data was received
  #
  if len(lineOfData) > 0:
    pos1, pos2, sensorValue = (int(x) for x in lineOfData.split(','))

    distance = getDistance(sensorValue)
    
    data.append(pos1)
    data.append(pos2)
    data.append(distance)

    with open(dataFile, 'a', newline='') as csvfile:
      csvWriter = csv.writer(csvfile,delimiter=',')
      csvWriter.writerow(data)
      data = []
