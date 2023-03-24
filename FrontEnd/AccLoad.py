num_of_slots=8
title="ma41"

from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox


window = Tk()
window.title(title)
window.title(title+" - "+"com4")


frm=[]
stx=[]
lbl=[]
btn=[]

def reset():
    pass


for i in range(0,num_of_slots):
    frm.append(Frame(window))

    stx.append(scrolledtext.ScrolledText(frm[i],width = 20,height = 40))
    stx[i].pack()

    lbl.append(Label(frm[i],text="Ожидание"))
    lbl[i].pack()

    btn.append(Button(frm[i],text="Сброс",command=reset))
    btn[i].pack()
    
    frm[i].pack(side=LEFT)

for i in range(0,num_of_slots):
    stx[i].insert(INSERT,"МАУП "+str(i))    
