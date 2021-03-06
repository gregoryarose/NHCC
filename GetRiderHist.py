#!/usr/bin/env python

from cosmosdb_sdk import CosmosDB
import json
import numpy as np
import pandas as pd
import sys
from datetime import datetime
from datetime import timedelta


pd.set_option('display.colheader_justify', 'center')

cosmosDBName = 'Grading'
containerName = 'Rider'
dbConnection = CosmosDB(cosmosDBName, containerName)
 
def GetHist(License):

    PointsExpire = 183
    FreezeDate = "2022-04-27"
    if datetime.today().strftime('%Y-%m-%d') < FreezeDate:
        PointsExpire +=85


    query = 'SELECT c.FirstName, c.Surname,c.Grade,t.RaceGrade,t.RaceDate,t.RaceResult ?? "-" as RaceResult ,t.RacePoints ?? "" as Points FROM c JOIN t IN c.RaceEntry WHERE c.License = ' + str(License)  
    #print(query)
    try:
        results = dbConnection.query_item(query)
        df = pd.DataFrame(results, columns=None)
        RiderName = df.at[0, "FirstName"] + " " + df.at[0, "Surname"] + " - Current Grade: " + df.at[0, "Grade"]
        #Get rid of nulls'
        df2 = df.replace(np.nan, "")
    except Exception as e:
        print(str(e))

   
    #sort by race date descending
    sorted_df = df2.sort_values(by='RaceDate', ascending=False)
    left_aligned_df = df.style.set_properties(**{'text-align': 'left'})
    
    query2 = 'SELECT VALUE root FROM (SELECT sum(t.RacePoints) as Active_Points FROM c JOIN t IN c.RaceEntry WHERE  t.RaceGrade <= c.Grade  and DateTimeDiff("day", t.RaceDate, GetCurrentDateTime ()) <= ' + str(PointsExpire) + ' and c.License = ' + str(License)+ ' )as root ' 
    #print(query2)
    try:
        results2 = dbConnection.query_item(query2)
        df3 = pd.DataFrame(results2, columns=None)
        selection = sorted_df[['RaceGrade', 'RaceDate', 'RaceResult','Points']]
    except Exception as e:
        print(str(e))
    
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
    try:
        results = dbConnection.query_item(query)       
        df = pd.DataFrame(results, columns=None)
        dflist = df.values.tolist()
    except Exception as e:
        print(str(e))


    return df
  
    
def GetGrades():

    PointsExpire = 183
    FreezeDate = "2022-04-27"
    if datetime.today().strftime('%Y-%m-%d') < FreezeDate:
        PointsExpire +=85
 
    query = 'SELECT VALUE root FROM (SELECT c.Grade, UPPER(c.Surname) as Surname, c.FirstName,c.club, '
    query += 'sum((t.RaceGrade <= c.Grade and DateTimeDiff("day", t.RaceDate, GetCurrentDateTime ()) <= ' + str(PointsExpire) +' )? t.RacePoints:0) as Points FROM c  JOIN t IN c.RaceEntry '
    query += 'Group By c.Grade, c.Surname, c.FirstName,c.club)as root ' 
    
    try:
        results = dbConnection.query_item(query)     
        df = pd.DataFrame(results, columns=None)
        sorted_df = df.sort_values(by=['Surname','FirstName'],ignore_index=True)
        
    except Exception as e:
        print(str(e))   
        
    return sorted_df

def GetTopPoints():
    PointsExpire = 183
    FreezeDate = "2022-04-27"
    if datetime.today().strftime('%Y-%m-%d') < FreezeDate:
        PointsExpire +=85

# point expirey is usally 6 months - due to covid break extra days allowed till this date

 
    query = 'SELECT VALUE root FROM (SELECT c.Grade, c.Surname, c.FirstName,c.club, '
    query += 'sum((t.RaceGrade <= c.Grade and DateTimeDiff("day", t.RaceDate, GetCurrentDateTime ()) <= ' + str(PointsExpire) +' )? t.RacePoints:0) as Points FROM c  JOIN t IN c.RaceEntry '
    query += 'Group By c.Grade, c.Surname, c.FirstName,c.club)as root where root.Points >= 8 ' 
    
    try:
        results = dbConnection.query_item(query)     
        df = pd.DataFrame(results, columns=None)
        sorted_df = df.sort_values(by=['Grade','Points'],ascending = [True, False])
    except Exception as e:
        print(str(e))   
        
    return sorted_df
    
def GetRace():
    query = 'SELECT VALUE root FROM (SELECT distinct t.RaceDate,t.RaceType,t.RaceVenue, CONCAT("#",ToString(t.RaceID)) as RaceID FROM c JOIN t IN c.RaceEntry )as root   ' 
    
    try:
        results = dbConnection.query_item(query)     
        df = pd.DataFrame(results, columns=None)
        sorted_df = df.sort_values(by='RaceDate',ascending = False,ignore_index=True)
        
    except Exception as e:
        print(str(e))   
        
    return sorted_df  
    
def GetRaceResults(RID):
 
    query = 'SELECT VALUE root FROM (SELECT distinct t.RaceGrade, t.RaceResult, c.FirstName, c.Surname ,SUBSTRING(c.Club,0,8) as Club FROM c  '
    query += 'JOIN t IN c.RaceEntry where LENGTH(t.RaceResult) > 0 and t.RaceID = ' + RID +' )as root   ' 
    
    try:
        results = dbConnection.query_item(query)     
        df = pd.DataFrame(results, columns=None)
        #print(df)
        sorted_df = df.sort_values(by=['RaceGrade','RaceResult'],ascending = [True, True],ignore_index=True)
        #sorted_df = df.sort_values(by=['RaceGrade','RaceResult'],ascending = [True, True])
        sorted_df.set_index('RaceGrade', inplace=True)
    except Exception as e:
        print(str(e))   
        
    return sorted_df   



