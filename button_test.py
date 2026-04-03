# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 14:26:02 2025

@author: Zen
"""

from tkinter import *
class InterActiveButton:
    def __init__(self,root):
        self.root = root
        self.root.geometry("800x600")

        self.button1=Button(self.root,bg="dark blue",fg="#dad122",cursor="hand2",text="Button 1",font=("arial",18,"bold"),bd=0,activebackground="dark blue",activeforeground="#dad122")
        self.button1.place(x=10,y=10,width=200,height=50)
        self.button1.bind("<Enter>",self.on_hover)
        self.button1.bind("<Leave>",self.on_leave)
        
        self.button3=Button(self.root,bg="dark blue",fg="#dad122",cursor="hand2",text="Button 2",font=("arial",18,"bold"),bd=0,activebackground="dark blue",activeforeground="#dad122")
        self.button3.place(x=230,y=10,width=200,height=50)
        self.button3.bind("<Enter>",self.on_hover)
        self.button3.bind("<Leave>",self.on_leave)
        
        self.button3=Button(self.root,bg="dark blue",fg="#dad122",cursor="hand2",text="Button 3",font=("arial",18,"bold"),bd=0,activebackground="dark blue",activeforeground="#dad122")
        self.button3.place(x=450,y=10,width=200,height=50)
        self.button3.bind("<Enter>",self.on_hover)
        self.button3.bind("<Leave>",self.on_leave)
    def increase_width(self,ev):
        if self.done!=12:
            ev.place_configure(width=200+self.done)
            self.width_b=200+self.done
            print(self.width_b)
            self.done+=1
            self.root.after(5,lambda:self.increase_width(ev))
    def decrease_width(self,ev):
        if self.done!=12:
            ev.place_configure(width=self.width_b-1)
            self.width_b=self.width_b-1
            print("-------------")
            print(self.width_b)
            self.done+=1
            self.root.after(5,lambda:self.decrease_width(ev))
    def on_hover(self,event,*args):
        self.done=0
        event.widget['bg']="#dad122"
        event.widget['fg']="dark blue"
        #event.widget.place_configure(width=210,height=55)
        self.root.after(5,lambda: self.increase_width(event.widget))
    def on_leave(self,event,*args):
        self.done=0
        event.widget['fg']="#dad122"
        event.widget['bg']="dark blue"
        #event.widget.place_configure(width=200,height=50)
        self.root.after(5,lambda: self.decrease_width(event.widget))
        
root=Tk()
ob=InterActiveButton(root)
root.mainloop()