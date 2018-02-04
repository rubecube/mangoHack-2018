import os
import time
import zmq
from matrix_io.proto.malos.v1 import driver_pb2 , io_pb2
from matrix_io.proto.malos.v1 import io_pb2


import socket
data_from_socket = 'h'
bind_ip = "0.0.0.0"
bind_port = 5022
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))
server.listen(2)
print "[*] Listening on %s:%d" % (bind_ip,bind_port)

def handle_client():
	sock, addr = server.accept()
	request = sock.recv(200)
	global data_from_socket
	data_from_socket = request
	print "[*] Received : %s" % request

def callLights(red,blue,green,white,valueSim):
  creator_ip = os.environ.get('CREATOR_IP', '127.0.0.1')
  creator_everloop_base_port = 20013 + 8
  creator_gpio_base_port = 20013 + 36

  context = zmq.Context()
  config = driver_pb2.DriverConfig()
  socket = context.socket(zmq.PUSH)
  socket.connect('tcp://{0}:{1}'.format(creator_ip, creator_everloop_base_port))
  image = []
  socket.connect('tcp://{0}:{1}'.format(creator_ip, creator_gpio_base_port))
  config.gpio.pin = 15
  config.gpio.mode = io_pb2.GpioParams.OUTPUT

  # iterate over all 35 LEDS and set the rgbw value of each
  # then append it to the end of the list/image thing
  for led in range(35):
      ledValue = io_pb2.LedValue()
      ledValue.blue = blue
      ledValue.red = red
      ledValue.green = green
      ledValue.white = white
      image.append(ledValue)

  config.gpio.value = valueSim

  config.image.led.extend(image)
  

  socket.send(config.SerializeToString())

def gpioPin(value):
	creator_ip = os.environ.get('CREATOR_IP', '127.0.0.1')
	creator_gpio_base_port = 20013 + 36
	context = zmq.Context()
	socket = context.socket(zmq.PUSH)
	socket.connect('tcp://{0}:{1}'.format(creator_ip, creator_gpio_base_port))
	config = driver_pb2.DriverConfig()
	config.gpio.pin = 15
	config.gpio.mode = io_pb2.GpioParams.OUTPUT
	config.gpio.value = value
	socket.send(config.SerializeToString())
	time.sleep(1)	


CODE = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
     	'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
        
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.' 
        }
def timecall(delayTime):
	callLights(112,123,125,50,1)
	gpioPin(1)
	time.sleep(delayTime)
	callLights(0,0,0,0,0)
	gpioPin(0)

	

def main():
	#msg = raw_input('MESSAGE: ')
	
	handle_client()
	print "ager handler "+ data_from_socket
	for char in data_from_socket:
		print CODE[char.upper()]+'\n'
		for x in CODE[char.upper()]:	
			if x == '.':
				timecall(.15)
			if x == '-':
				timecall(.45)
			time.sleep(.2)
		time.sleep(.4)
if __name__ == "__main__":
	main()
	#timecall(2)
