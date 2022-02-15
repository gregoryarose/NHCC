#!/usr/bin/env python

from cosmosdb_sdk import CosmosDB
import json
import numpy as np
import pandas as pd
import sys

cosmosDBName = 'Grading'
containerName = 'Rider'

#dbConnection = CosmosDB(cosmosDBName, containerName)

 
def main():
    args = sys.argv[1:]
    license = args[0]
    dbConnection = CosmosDB(cosmosDBName, containerName)

    #license = 511881
    query = 'SELECT c.FirstName, c.Surname,c.Grade,t.RaceGrade,t.RaceDate,t.RaceResult,t.RacePoints as Points FROM c JOIN t IN c.RaceEntry WHERE c.License = ' + str(license)  
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
    sorted_df = df2.sort_values(by='RaceDate', ascending=True)
    
    query2 = 'SELECT VALUE root FROM (SELECT sum(t.RacePoints) as Active_Points FROM c JOIN t IN c.RaceEntry WHERE DateTimeDiff("day", t.RaceDate, GetCurrentDateTime ()) <= 269 and c.License = ' + str(license)+ ' )as root ' 
    results2 = dbConnection.query_item(query2)
    df3 = pd.DataFrame(results2, columns=None)
    selection = sorted_df[['RaceGrade', 'RaceDate', 'RaceResult','Points']]
    print() #blank line
    print("Rider History Report: " + RiderName)
    print() #blank line
    print(selection.to_string()) 
    print('- ' * 30)  
    print(df3)
    
if __name__=="__main__":
    main()
  


    
  