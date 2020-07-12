import serial

ser_display = serial.Serial('COM16', 9600, timeout=0.01, write_timeout=0)

while True:
    tmp = ser_display.readline().decode('utf-8','ignore')
    if len(tmp):
        print(tmp)