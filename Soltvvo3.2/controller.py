# coding:utf-8
import serial
import RPi.GPIO as GPIO
from time import time

# アクチュエータを動かすコマンドを送る
# Send commands to move actuators
def move_actuator(num, arg1, arg2, arg3=None):
    if arg3 == None:
        com = str(arg1) + ' ' + str(arg2)
    else:
        com = str(arg1) + ' ' + str(arg2) + ' ' + str(arg3)
    ser_motor[num].write((com + '\n').encode())

# キューブを掴む
# Grab arms
def grab_p():
    for i in range(2):
        for j in range(2):
            move_actuator(j, i, 1000)
        sleep(3)

# キューブを離す
# Release arms
def release_p():
    for i in range(2):
        for j in range(2):
            move_actuator(i, j, 2000)

# アームのキャリブレーション
# Calibration arms
def calibration():
    release_p()
    sleep(0.1)
    for i in range(2):
        for j in range(2):
            move_actuator(j, i, 0, 500)

# 実際にロボットを動かす
# Move robot
def controller(slp1, slp2, rpm, ratio, solution):
    global ans
    strt_solv = time()
    for i, twist in enumerate(solution):
        if GPIO.input(21) == GPIO.LOW:
            if bluetoothmode:
                client_socket.send('emergency\n')
            solvingtimevar.set('emergency stop')
            print('emergency stop')
            return
        if i != 0:
            grab = twist[0][0] % 2
            for j in range(2):
                move_actuator(j, grab, 1000)
            sleep(slp1)
            for j in range(2):
                move_actuator(j, (grab + 1) % 2, 2000)
            sleep(slp2)
        max_turn = 0
        for each_twist in twist:
            ser_num = twist[0] // 2
            move_actuator(ser_num, ans[i][0] % 2, ans[i][1] * 90, rpm)
            max_turn = max(abs(each_twist[1]))
        slptim = 2 * 60 / rpm * (max_turn * 90 - offset) / 360 * ratio
        sleep(slptim)
    solv_time = str(int((time() - strt_solv) * 1000) / 1000).ljust(5, '0')
    return solv_time

ser_motor = [None, None]

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN)
ser_motor[0] = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01, write_timeout=0)
ser_motor[1] = serial.Serial('/dev/ttyUSB1', 115200, timeout=0.01, write_timeout=0)

print('controller initialized')