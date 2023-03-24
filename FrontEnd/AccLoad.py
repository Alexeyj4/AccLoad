num_of_slots=8
title="ma41"

from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import serial

window = Tk()
window.title(title)

#debug
window.title(title+" - "+"com5")

frm=[]

lbl_name=[]
lbl_u=[]
lbl_i=[]
stx=[]
lbl_status=[]
btn=[]

def reset():
    pass

#debug
ser = serial.Serial("COM5")

for i in range(0,num_of_slots):
    frm.append(Frame(window))

    lbl_name.append(Label(frm[i],text="МАУП"+str(i)))
    lbl_name[i].pack()

    lbl_u.append(Label(frm[i],text="U="))
    lbl_u[i].pack()

    lbl_i.append(Label(frm[i],text="I="))
    lbl_i[i].pack()

    stx.append(scrolledtext.ScrolledText(frm[i],width = 20,height = 40))
    stx[i].pack()

    lbl_status.append(Label(frm[i],text="Ожидание"))
    lbl_status[i].pack()

    btn.append(Button(frm[i],text="Сброс",command=reset))
    btn[i].pack()
    
    frm[i].pack(side=LEFT)

for i in range(0,num_of_slots):
    stx[i].insert(INSERT,"МАУП "+str(i))    

def loop1():
    stx[1].insert(INSERT,ser.read())
    window.after(5, loop1)      

        
loop1()

#window.mainloop()
