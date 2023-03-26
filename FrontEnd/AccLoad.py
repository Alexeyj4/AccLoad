num_of_slots=8
title="ma41"
port="com5"

from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import serial

window = Tk()
window.title(title)

#debug
window.title(title+" - "+port)

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
ser = serial.Serial(port,9600,timeout=0)

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

    if ser.inWaiting()==0:
        window.title(title+" - "+port+" OFFLINE")
    else:
        window.title(title+" - "+port+" online")
        while ser.inWaiting()>0:
            received=ser.read();
            #stx[1].insert(INSERT,received) #debug
            if received=='s':
                stx[1].insert(INSERT,"SSS")       #debug
                slot_c=ser.readline()
                
                if slot_c!='' and int(slot_c)>=0 and int(slot_c)<num_of_slots:
                    slot_i=int(slot_c)
                    lbl_u[slot_i]['text']=ser.readline()
                    lbl_i[slot_i]['text']=ser.readline()
                
                    
                    

            
    stx[1].insert(INSERT,ser.readline())       #debug
    
    

    window.after(100, loop1)
    
loop1()

window.mainloop()
