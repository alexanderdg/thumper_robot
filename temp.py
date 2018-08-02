import serial

ser=serial.Serial(port='/dev/ttyUSB0', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1 )

data_to_send = "1:{0}\n".format(str(255))
self.ser.write(data_to_send)

