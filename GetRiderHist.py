#!/usr/bin/env python

from cosmosdb_sdk import CosmosDB
import json
import numpy as np
import pandas as pd
import sys
pd.set_option('display.colheader_justify', 'center')

cosmosDBName = 'Grading'
containerName = 'Rider'
dbConnection = CosmosDB(cosmosDBName, containerName)
 
def GetHist(License):


    query = 'SELECT c.FirstName, c.Surname,c.Grade,t.RaceGrade,t.RaceDate,t.RaceResult ?? "-" as RaceResult ,t.RacePoints ?? "" as Points FROM c JOIN t IN c.RaceEntry WHERE c.License = ' + str(License)  
    print(query)
    try:
        results = dbConnection.query_item(query)
        
    except Exception as e:
        print(str(e))
    df = pd.DataFrame(results, columns=None)
    
    RiderName = df.at[0, "FirstName"] + " " + df.at[0, "Surname"] + " - Current Grade: " + df.at[0, "Grade"]
    
    #Get rid of nulls'
    df2 = df.replace(np.nan, "")
   
    #print(df2)

    #df2.RaceResult = [place[item] for item in df2.RaceResult]
    #df2.RacePoints = [point[item] for item in df2.RacePoints]
   
    #sort by race date descending
    sorted_df = df2.sort_values(by='RaceDate', ascending=False)
    left_aligned_df = df.style.set_properties(**{'text-align': 'left'})
    
    query2 = 'SELECT VALUE root FROM (SELECT sum(t.RacePoints) as Active_Points FROM c JOIN t IN c.RaceEntry WHERE  t.RaceGrade <= c.Grade  and DateTimeDiff("day", t.RaceDate, GetCurrentDateTime ()) <= 269 and c.License = ' + str(License)+ ' )as root ' 
    print(query2)
    results2 = dbConnection.query_item(query2)
    df3 = pd.DataFrame(results2, columns=None)
    #dfAlign = sorted_df.style.set_properties(**{'text-align': 'left'})
    
    
    selection = sorted_df[['RaceGrade', 'RaceDate', 'RaceResult','Points']]
    #selection = selection.style.set_properties(**{'text-align': 'left'})
    
    NewLine = '\n'
    
    MyString = "Rider History Report: "  + RiderName +  " \n"
    MyString = MyString +  " \n" + df3.to_string(index=False)
    MyString = MyString +  " \n" + '- ' * 30 + " \n"
    MyString = MyString + selection.to_string(index=False)
    MyString = MyString +  " \n" +  " \n" + '- ' * 30 + " \n" + " \n"
    return(MyString)

def GetRider(Nm):
    Surname = Nm.upper()
    query = 'SELECT distinct c.Surname,c.FirstName,c.Club, CONCAT("#", tostring(c.License)) as License FROM c where UPPER(c.Surname) like "' + Surname +'%"'
    #print(query)
    results = dbConnection.query_item(query)
        
    df = pd.DataFrame(results, columns=None)
    dflist = df.values.tolist()
    
    #MyString = df.to_string(index=False)
    #print(df)
    return df
    #return dflist  
    
def GetGrades():
 
    query = 'SELECT VALUE root FROM (SELECT c.Grade, c.Surname, c.FirstName,c.club, '
    query += 'sum((t.RaceGrade <= c.Grade and DateTimeDiff("day", t.RaceDate, GetCurrentDateTime ()) <= 269)? t.RacePoints:0) as Points FROM c  JOIN t IN c.RaceEntry '
    query += 'Group By c.Grade, c.Surname, c.FirstName,c.club)as root ' 
    
    #print(query)
    results = dbConnection.query_item(query)
        
    df = pd.DataFrame(results, columns=None)
    sorted_df = df.sort_values(by=['Surname','FirstName'])
    return sorted_df
    #return df
