import serial
import tkinter
from time import time

strt = 0
solv_flag = False

def main():
    global strt, solv_flag
    receive = ser_display.readline().decode('utf-8','ignore').replace('\n', '')
    if receive == 'start':
        strt = time()
        solv_flag = True
    elif receive == 'emergency':
        solvingtimevar.set('EMR')
        solv_flag = False
    elif len(receive):
        solvingtimevar.set(receive)
        solv_flag = False
    elif solv_flag:
        solvingtimevar.set(str(round(time() - strt, 3)))
    root.after(1, main)



ser_display = serial.Serial('COM16', 9600, timeout=0.01, write_timeout=0)

root = tkinter.Tk()
root.title("Soltvvo")
root.geometry("1000x800")

solvingtimevar = tkinter.StringVar(master=root, value='')
solvingtimevar.set('0.000')
solvingtime = tkinter.Label(textvariable=solvingtimevar,font=("",500))
solvingtime.place(x=200, y=200)

root.after(1, main)

root.mainloop()