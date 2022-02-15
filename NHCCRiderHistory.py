import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk, Menu
from tkinter.messagebox import showinfo
from cosmosdb_sdk import CosmosDB
import json
import numpy as np
import pandas as pd
import sys
import GetRiderHist
import os

#todo - scroll bars, license look up

  
root=tk.Tk()
 
# setting the windows size
root.geometry("900x900")
root['background']='#B9D687'
root.title("NHCC") 



my_menu=Menu(root)
root.config(menu=my_menu)

def GS_command():
    #clear_text()
    txt.delete("1.0", "end")
    strGrade = GetRiderHist.GetGrades()
    txt.insert("1.0",strGrade.to_string(index=False))
    #my_label = Label(root, text="Clicked!!").pack()
    #showinfo(title="Information", message="Hello World!")
    
def Top_Points_command():
    #clear_text()
    txt.delete("1.0", "end")
    strpoints = GetRiderHist.GetTopPoints()
    txt.insert("1.0",strpoints.to_string(index=False))
    
    

def about_command():
    openAboutWindow()
    
def instruction_command():
    openInstructionsWindow()
    
    

 
file_menu= Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Show Grade Sheet",command=GS_command)
#file_menu.add_separator()
file_menu.add_command(label="Show Top Rider Points",command=Top_Points_command)
file_menu.add_command(label="Exit",command=root.quit)


Top_Points_command
    
option_menu = Menu(my_menu)
my_menu.add_cascade(label="Help",menu=option_menu)
option_menu.add_command(label="About",command=about_command)
option_menu.add_command(label="Instruction",command=instruction_command)





##########################################################################################
# function to open a new window
# on a button click
def openNewWindow():
     
    # Toplevel object which will
    # be treated as a new window
    ws = tk.Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    ws.title("NHCC")
 
    # sets the geometry of toplevel
    ws.geometry("500x500")
 
    ws.config(bg='#CAEEBE')
    
    # Variable for storing name 
    Sname_var=tk.StringVar()
 
    # Create a Label widget
    Label(ws, text="Rider License Lookup", font=('Helvetica 16 bold'), background='#E3F0CE').pack(pady=20)
    
    # Add Field for Name
    Label(ws, font=('Helvetica 14'),text="Enter Surname:").pack(pady=10)
    Sname = Entry(ws,textvariable = Sname_var,font=('Helvetica 14')).pack(pady=10)
  
 
    
    SelectedLicense = '99999999'
    lb = tk.Listbox(ws,width = 70)
    
    

    def showSelected():
        #show.config(text=lb.get(ANCHOR))
        Lic = extractLicense()
        LicStrip= splitLicenseOut(Lic)
        SelectedLicense = LicStrip
        print(SelectedLicense)
        addToClipBoard(SelectedLicense)
        
        fname.delete(0, 'end') #deletes the current value
        fname.insert(0, SelectedLicense) #inserts new value assigned by 2nd parameter
        ws.destroy()
        
    def showRider():
        Rider_SName = Sname_var.get()       
        lst = GetRiderHist.GetRider(Rider_SName)     
        #lb = tk.Listbox(ws,width = 70)
        lb.pack()

        
        for index, row in lst.iterrows():
            s = lst.iloc[index,:].to_string(header=False, index=False)
            s = s.replace('\n',"  ")
            s = s.strip()
            lb.insert(index, s)
        Button(ws, text='Copy License', command=showSelected).pack(pady=20)

    def extractLicense():
        for i in lb.curselection():
           x=lb.get(i)
           return x   
        
    
    def splitLicenseOut(LS):
       LStart = LS.find("#")+1
       LEnd = len(LS)
       y = LS[LStart:LEnd]
       #print(y)
       return y
       
    def addToClipBoard(text):
       command = 'echo ' + text.strip() + '| clip'
       os.system(command)
    
     

    
    Button(ws, text='Find Rider', command=showRider).pack(pady=20)
    

#################################################################################


def openAboutWindow():
    
    strAbout = "Newcastle Hunter Cycling Club rider database and grading system." + "\n \n"
    strAbout += "Version 0.1 (14 Feb 2022)" + "\n \n" 
    strAbout += "Developed by Gregory Rose - gregory.rose@optusnet.com.au"
     
    # Toplevel object which will
    # be treated as a new window
    ws = tk.Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    ws.title("NHCC")
 
    # sets the geometry of toplevel
    ws.geometry("650x200")
    ws.config(bg='#CAEEBE')
    
    txtAbout= tk.Text(ws,font=('Calabri',12,'bold')) 
    
    txtAbout.insert("1.0",strAbout)
    txtAbout.pack(pady=10)
    


#################################################################################


#################################################################################


def openInstructionsWindow():
    
    strInstructions = "How to look up a rider." + "\n \n"
    strInstructions += "Type the rider license number (excluding any letters) into the Enter License text box.\nHit the Submit button.\n\n" 
    strInstructions += "If you don't know the Licence number, hit the Licence Lookup button.\n\nEnter the Surname or first few letters of the surname. \nClick the Find Rider button. \n\n"
    strInstructions += "Click on the rider you want in the list box. \nClick Copy License. \n\n"
     
    # Toplevel object which will
    # be treated as a new window
    ws = tk.Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    ws.title("NHCC")
 
    # sets the geometry of toplevel
    ws.geometry("700x300")
    ws.config(bg='#CAEEBE')
    
    txtAbout= tk.Text(ws,font=('Calabri',12,)) 
    
    txtAbout.insert("1.0",strInstructions)
    txtAbout.pack(pady=10)
    


#################################################################################





#Declaring string variable
# for storing name and password
name_var=tk.StringVar()

# Add a Frame widget
frame = tk.Frame(root)
frame['background']='#B9D687'

# Create a Label widget
tk.Label(frame, text="Newcastle Hunter Cycling Club Grading Info Tool", font=('Helvetica 16 bold'), background='#E3F0CE').grid(row=5, column=0, pady=30)
frame.pack()

  
# defining a function that will
# get the name and password and
# print them on the screen


def submit():
    #clear_text()
    txt.delete("1.0", "end")
    name=name_var.get()
    
    License=name_var.get() 
    strHist = GetRiderHist.GetHist(License)
    txt.insert("1.0",strHist)
    
     
     
# creating a label for
# name using widget Label
#name_label = tk.Label(root, text = 'Enter License Number:', font=('calibre',10, 'bold'))


heading_label = tk.Label(root, text = 'Newcastle Hunter Cycling Club Rider points and history tool.  Enter rider license (numbers only) in the box and hit the submit button ', font=('calibre',14, 'bold')) 
# creating a entry for input
# name using widget Entry
#name_entry = tk.Entry(root,textvariable = name_var, font=('calibre',10,'normal'))

# Add Field for License
#tk.Label(frame, font=('Helvetica 14'),text="Enter License:").grid(row=7, column=0, padx=5, pady=10)
fname = tk.Entry(frame,textvariable = name_var,font=('Helvetica 14'))
fname.grid(row=10, column=0, padx=10)

# Create a button
tk.Button(frame, text="Submit", command=submit, font=('Helvetica 14')).grid(row=15,column=0, padx=5, pady=10)

# a button widget which will open a
# new window on button click
tk.Button(frame, text ="Rider History", command = openNewWindow, font=('Helvetica 14')).grid(row=7,column=1, padx=5, pady=10)
tk.Button(frame, text ="Grade Sheet", command = GS_command, font=('Helvetica 14')).grid(row=8,column=1, padx=5, pady=10)
tk.Button(frame, text ="High Points", command = Top_Points_command, font=('Helvetica 14')).grid(row=9,column=1, padx=5, pady=10)
  
# placing the label and entry in
# the required position using grid
# method
#heading_label.grid(row=0,column=0)
#name_label.grid(row=1,column=0)
#name_entry.grid(row=2,column=0)
#sub_btn.grid(row=3,column=0)
txt= tk.Text(frame, height=41, width=60) 
# Attach the scrollbar with the text widget

# Add a Scrollbar(horizontal)
v=tk.Scrollbar(frame,  orient='vertical')
v.grid(row=20,column=1,sticky='NS')
v.config(command=txt.yview)
txt.grid(row=20,column=0)



root.mainloop()

