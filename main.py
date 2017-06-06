import serial
import requests

counter = 0
counter_max = 10
press_th = 0.9
th = [0, 0]
isPressed = [0, 0]

def press(room_number, status, priority):
  url = "http://133.16.123.101/api/sensor/" + str(room_number) + "/" + status + "/" + str(priority)
  r = requests.get(url)
  print r.status_code
  print r.text


ser = serial.Serial('/dev/tty.usbmodem1421', 115200, timeout=5.0)
while True:
  line = ser.readline()
  if line != "":
    data = line.split(',')
    data[0] = int(data[0])
    data[1] = int(data[1])
    if counter < counter_max:
      th[0] += data[0]
      th[1] += data[1]
      counter += 1
    elif counter == counter_max:
      th[0] = th[0] / counter_max * 0.8
      th[1] = th[1] / counter_max * 0.8
      counter += 1
      print "Threadhold"
      print th[0]
      print th[1]
    else:
      #print (str(data[0]) + ", " + str(data[1]))
      if(data[0] < th[0] and isPressed[0] == 0):
        print ("Priority 0 pressed")
        press(101, "active", 1)
        isPressed[0] = 1
      elif(data[0] > th[0]):
        isPressed[0] = 0

      if(data[1] < th[1] and isPressed[1] == 0):
        print ("Priority 1 pressed")
        press(101, "active", 2)
        isPressed[1] = 1
      elif(data[1] > th[1]):
        isPressed[1] = 0

ser.close()



