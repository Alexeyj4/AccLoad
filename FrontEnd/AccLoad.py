#num_of_slots=8
title="APEX Acc tester v1.0"
#port="com11"

meas_threshold=0.08

from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import serial
from functools import partial
import time
import configparser

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг
num_of_slots=int(config['settings']['num_of_slots'])
port=config["settings"]["port"]

amper_hour_min_norma=float(config["settings"]["amper_hour_min_norma"])
amper_hour_max_norma=float(config["settings"]["amper_hour_max_norma"])
Umin_norma=float(config["settings"]["Umin_norma"])
Umax_norma=float(config["settings"]["Umax_norma"])
Imin_norma=float(config["settings"]["Imin_norma"])
Imax_norma=float(config["settings"]["Imax_norma"])

window = Tk()
window.title(title)

window.title(title+" - "+port)

frm=[]
lbl_name=[]
lbl_u=[]
lbl_i=[]
stx=[]
lbl_status=[]
btn=[]

umin=[]
umax=[]
imin=[]
imax=[]

slot_status=[]
slot_start_time=[]

def reset_slot(slot_num):
    umin[slot_num]=127;
    umax[slot_num]=0;
    imin[slot_num]=127;
    imax[slot_num]=0;
    slot_status[slot_num]='standby'
    lbl_status[slot_num].config(text="Ожидание",background='white')    

def reset_press(slot_num):
    stx[slot_num].delete('1.0', END)
    reset_slot(slot_num)
    pass

def readser(): #read string from serial and delete escape symbols
    received_string=ser.readline()
    
    if received_string=='':
        return ''
    res_string=''
    i=0
    while(received_string[i]!=13 and received_string[i]!=10):    #!= \r \n
        res_string=res_string+chr(received_string[i])
        i=i+1
    return res_string

ser = serial.Serial(port,9600)

for i in range(0,num_of_slots):

    umin.append(127);
    umax.append(0);
    imin.append(127);
    imax.append(0);
    slot_start_time.append(time.time());

    slot_status.append('standby'); #standby/discharge/complete
    
    
    frm.append(Frame(window))

    lbl_name.append(Label(frm[i],text="Ячейка"+str(i)))
    lbl_name[i].pack()

    lbl_u.append(Label(frm[i],text="U="))
    lbl_u[i].pack()

    lbl_i.append(Label(frm[i],text="I="))
    lbl_i[i].pack()

    stx.append(scrolledtext.ScrolledText(frm[i],width = 20,height = 40))
    stx[i].pack()

    lbl_status.append(Label(frm[i],text="Не работает",font='bold'))
    lbl_status[i].pack()

    btn.append(Button(frm[i],text="Сброс",command=partial(reset_press, i))) 
    btn[i].pack()
    
    frm[i].pack(side=LEFT)
  

def loop1():
    if ser.inWaiting()==0:
        window.title(title+" - "+port+" OFFLINE")
    else:
        window.title(title+" - "+port+" online")
        while ser.inWaiting()>0:
            received=readser();
            
            if received=='slot':            
                slot_c=readser()
                
                if len(slot_c)==1 and slot_c!='' and int(slot_c)>=0 and int(slot_c)<num_of_slots:
                    slot_i=int(slot_c)
                    try:
                        u=float(readser())
                        i=float(readser())
                        skip=0
                    except: #error in received data
                        stx[slot_i].insert(INSERT,'Error\n')
                        skip=1
                        

                    if skip==0:
                        lbl_u[slot_i]['text']='U='+str(u)
                        lbl_i[slot_i]['text']='I='+str(i)

                        if u>meas_threshold or i>meas_threshold:        #есть ток или напряжение

                            if slot_status[slot_i]=='standby':
                                slot_start_time[slot_i]=time.time()
                                stx[slot_i].insert(INSERT,'Начало разряда:\n')
                                minutes=str(time.localtime(time.time()).tm_min)                                
                                if len(minutes)==1: minutes='0'+minutes
                                stx[slot_i].insert(INSERT,str(time.localtime(time.time()).tm_hour)+':'+minutes+'\n')
                                lbl_status[slot_i].config(text="Разряд",background='yellow')
                                slot_status[slot_i]='discharge'                                
                            
                            if slot_status[slot_i]=='discharge':
                                stx[slot_i].insert(INSERT,str(u)+'/'+str(i)+'\n')
                                if u<umin[slot_i]:
                                    umin[slot_i]=u
                                if u>umax[slot_i]:
                                    umax[slot_i]=u                                
                                if i<imin[slot_i]:
                                    imin[slot_i]=i
                                if i>imax[slot_i]:
                                    imax[slot_i]=i                                
                        else:                                       #нет тока или напряжения                      

                            if slot_status[slot_i]=='discharge':
                                stx[slot_i].insert(INSERT,'Конец разряда:\n')
                                
                                minutes=str(time.localtime(time.time()).tm_min)                                
                                if len(minutes)==1: minutes='0'+minutes
                                stx[slot_i].insert(INSERT, str(time.localtime(time.time()).tm_hour)+':'+minutes+'\n')
                                stx[slot_i].insert(INSERT,"Umin="+str(umin[slot_i])+'\n')
                                stx[slot_i].insert(INSERT,"Umax="+str(umax[slot_i])+'\n')
                                stx[slot_i].insert(INSERT,"Imin="+str(imin[slot_i])+'\n')
                                stx[slot_i].insert(INSERT,"Imax="+str(imax[slot_i])+'\n')
                                stx[slot_i].insert(INSERT,'Время разряда:\n')
                                t_dsch_sec=time.time()-slot_start_time[slot_i]                                
                                stx[slot_i].insert(INSERT,str(round(t_dsch_sec/60,2))+' мин\n')                                
                                stx[slot_i].insert(INSERT,'Ёмкость:\n')
                                ah=round(t_dsch_sec/3600*((imin[slot_i]+imax[slot_i])/2),2)
                                stx[slot_i].insert(INSERT,str(ah)+'А-ч')

                                ok=1
                                if ah<amper_hour_min_norma: ok=0
                                if ah>amper_hour_max_norma: ok=0
                                if umin[slot_i]<Umin_norma: ok=0
                                if umax[slot_i]>Umax_norma: ok=0
                                if imin[slot_i]<Imin_norma: ok=0
                                if imax[slot_i]>Imax_norma: ok=0

                                reset_slot(slot_i)
                                if ok==1:   
                                    slot_status[slot_i]='complete'
                                    lbl_status[slot_i].config(text="Годен!",background='green')
                                else:
                                    slot_status[slot_i]='complete'
                                    lbl_status[slot_i].config(text="Не годен!",background='red')
                                
              

    
    

    window.after(100, loop1)
    
loop1()

window.mainloop()
