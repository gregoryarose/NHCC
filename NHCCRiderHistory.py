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
 
# set the main windows Properites
root.geometry("900x900")
root['background']='#B9D687'
root.title("NHCC") 
p1 = tk.PhotoImage(file = 'NHCC.png')
  
# Setting icon of master window
root.iconphoto(False, p1)
root.grid_columnconfigure(0, weight=1)  

#Set up Menu
my_menu=Menu(root)
root.config(menu=my_menu)

#Declaring string variable for storing License number
global Lic_var
Lic_var=tk.StringVar()

global RD_var
RD_var=tk.StringVar()

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
    
def Race_Result_command():
    openNewWindowRace()
    
    
#Comfigure menu
 
file_menu= Menu(my_menu)
    
option_menu = Menu(my_menu)
my_menu.add_cascade(label="Help",menu=option_menu)
option_menu.add_command(label="About",command=about_command)
option_menu.add_command(label="Instruction",command=instruction_command)





##########################################################################################
# function to open a new window to look up license

def openNewWindow():
     
    # Toplevel object which will
    # be treated as a new window
    ws = tk.Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    ws.title("NHCC")
    p1 = tk.PhotoImage(file = 'NHCC.png')
  
    # Setting icon of master window
    ws.iconphoto(False, p1)
 
    # sets the geometry of toplevel
    ws.geometry("500x500")
 
    ws.config(bg='#CAEEBE')
    
    # Variable for storing name 
    Sname_var=tk.StringVar()
 
    # Create a Label widget
    Label(ws, text="Rider License Lookup", font=('Helvetica 16 bold'), background='#E3F0CE').pack(pady=20)
    
    # Add Field for Name
    Label(ws, font=('Helvetica 14'),text="Enter Surname:").pack(pady=10)
    RDate = Entry(ws,textvariable = Sname_var,font=('Helvetica 14')).pack(pady=10)
      
    SelectedLicense = '99999999'
    lb = tk.Listbox(ws,width = 70)
    
    

    def showSelected():
      try:
        global Lic_var
        txt.delete("1.0", "end")
        #show.config(text=lb.get(ANCHOR))
        Lic = extractLicense()
        LicStrip= splitLicenseOut(Lic)
        SelectedLicense = LicStrip
        #print(SelectedLicense)
        addToClipBoard(SelectedLicense)
        Lic_var = SelectedLicense
        
        #fname.delete(0, 'end') #deletes the current value
        #fname.insert(0, SelectedLicense) #inserts new value assigned by 2nd parameter
        strHist = GetRiderHist.GetHist(Lic_var)
        txt.insert("1.0",strHist)
        ws.destroy()
      except AttributeError:
        showinfo(title="Information", message="Please try again - choose a name first")
        ws.focus_set()
      except Exception as e:
        showinfo(title="Information", message=str(e))   
        ws.focus_set()        
    def showRider():
      Rider_SName = Sname_var.get()
      if len(Rider_SName) > 0:
    
          try:
            lb.delete(0,'end')             
            lst = GetRiderHist.GetRider(Rider_SName)     
            #lb = tk.Listbox(ws,width = 70)
            lb.pack(expand=True)
            
            for index, row in lst.iterrows():
                s = lst.iloc[index,:].to_string(header=False, index=False)
                s = s.replace('\n',"  ")
                s = s.strip()
                lb.insert(index, s)
            lb.select_set(0)
            Button(ws, text='Submit', command=showSelected).pack(pady=20)
          except Exception as e:
            print(str(e))
            showinfo(title="Information", message=str(e))
            
      else:
          showinfo(title="Information",message = "Please insert surname or part surname first")         
          ws.focus_set()

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


##########################################################################################
# function to open a new window to look up race results

def openNewWindowRace():
     
    # Toplevel object which will
    # be treated as a new window
    ws = tk.Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    ws.title("NHCC")
    p1 = tk.PhotoImage(file = 'NHCC.png')
  
    # Setting icon of master window
    ws.iconphoto(False, p1)
 
    # sets the geometry of toplevel
    ws.geometry("500x450")
 
    ws.config(bg='#CAEEBE')
    
    # Variable for storing name 
    RDate_var=tk.StringVar()
 
    # Create a Label widget
    Label(ws, text="Race Result Lookup", font=('Helvetica 16 bold'), background='#E3F0CE').grid(row=0,column=1,pady=20 )
    
      
    SelectedRace = '99999999'
    rd = tk.Listbox(ws,width = 70)
    # Add a Scrollbar(horizontal)
    v=tk.Scrollbar(ws,  orient='vertical')
    v.config(command=rd.yview)

    

    def showSelected():
      try:
        global RD_var
        txt.delete("1.0", "end")
        RID = extractRace()
        RD_var= splitIDOut(RID)
        strRace = GetRiderHist.GetRaceResults(RD_var)
        txt.insert("1.0",strRace)
        ws.destroy()
      except AttributeError:
        showinfo(title="Information", message="Please try again - choose a race")
        ws.focus_set()
      except Exception as e:
        showinfo(title="Information", message=str(e))   
        ws.focus_set()  
          
    def fillRaceList():
  
          try:
            rd.delete(0,'end')             
            lst = GetRiderHist.GetRace()     
            #lb = tk.Listbox(ws,width = 70)
            rd.grid(row=1,column=0,columnspan=3)
            v.grid(row=1,column=3,sticky= 'n'+'s')
            
            for index, row in lst.iterrows():
                s = lst.iloc[index,:].to_string(header=False, index=False)
                s = s.replace('\n',"  ")
                s = s.strip()
                rd.insert(index, s)
            rd.select_set(0)
            
          except Exception as e:
            print(str(e))
            showinfo(title="Information", message=str(e))
            


    def extractRace():
        for i in rd.curselection():
           x=rd.get(i)
           return x   
        
    

    def addToClipBoard(text):
       command = 'echo ' + text.strip() + '| clip'
       os.system(command)
       
    def splitIDOut(LS):
       LStart = LS.find("#")+1
       LEnd = len(LS)
       y = LS[LStart:LEnd]
       #print(y)
       return y    
     
    fillRaceList()

    Button(ws, text='Submit', command=showSelected).grid(row=2,column=1 , pady=20)
 
    
    

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
    strInstructions += "Click on 'Rider History'.\n\n" 
    strInstructions += "Enter the Surname or first few letters of the surname. \nClick the Find Rider button. \n\n"
    strInstructions += "Click on the rider you want in the list box. \nClick Submit. \n\n"
    strInstructions += "For all other functions just click the relevant button.\n\n"
     
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

#Set up 3 frames to layout objects


frame = tk.Frame(root)
frame['background']='#B9D687'
frame.pack()

frame1 = tk.Frame(root)
frame1['background']='#B9D687'
frame1.pack()

frame2 = tk.Frame(root)
frame2['background']='#B9D687'
frame2.pack()

# Submit button (button requirement removed - rolled into "Showselected")
def submit():
    #clear_text()
    txt.delete("1.0", "end")
    #name=name_var.get()
    
    #License=Lic_var.get() 
    License=Lic_var
    #print("LIcense from submit: "+License)
    strHist = GetRiderHist.GetHist(License)
    txt.insert("1.0",strHist)
    
 # Create a Label widget
tk.Label(frame, text="Newcastle Hunter Cycling Club Grading Info Tool", font=('Helvetica 16 bold'), background='#E3F0CE').grid(row=0, columnspan=3, pady=30)
#frame.pack()    

#heading_label = tk.Label(root, text = 'Newcastle Hunter Cycling Club Rider points and history tool.  Enter rider license (numbers only) in the box and hit the submit button ', font=('calibre',14, 'bold')) 


# Add Field for License
#tk.Label(frame, font=('Helvetica 14'),text="Enter License:").grid(row=7, column=0, padx=5, pady=10)
#fname = tk.Entry(frame2,textvariable = Lic_var,font=('Helvetica 14'))
#fname.grid(row=0, column=0, padx=10)

# Create a button
#tk.Button(frame2, text="Submit", activebackground='#78d6ff',command=submit, font=('Helvetica 14')).grid(row=1,column=0, padx=5, pady=10)

# a button widget which will open a
# new window on button click
tk.Button(frame1, text ="Rider History",  width = 15, activebackground='#78d6ff', command = openNewWindow, font=('Helvetica 14')).grid(row=0,column=0, padx=5, pady=10)
tk.Button(frame1, text ="Grade Sheet" , width = 15, activebackground = "#78d6ff", command = GS_command, font=('Helvetica 14')).grid(row=0,column=1, padx=5, pady=10)
tk.Button(frame1, text ="High Points", width = 15,activebackground = "#78d6ff", command = Top_Points_command, font=('Helvetica 14')).grid(row=1,column=0, padx=5, pady=10)
tk.Button(frame1, text ="Race Day Results",width = 15, activebackground = "#78d6ff", command = Race_Result_command, font=('Helvetica 14')).grid(row=1,column=1, padx=5, pady=10)  

txt= tk.Text(frame2, height=41, width=60) 
# Attach the scrollbar with the text widget

# Add a Scrollbar(horizontal)
v=tk.Scrollbar(frame2,  orient='vertical')
v.grid(row=3,column=2,sticky='NS')
v.config(command=txt.yview)
txt.grid(row=3,column=0 ,columnspan=2, sticky='w'+'e')


root.mainloop()



