from az.cli import az
from collections import namedtuple
import pandas as pd
from tabulate import tabulate

id_lis=[]
WorkItemType_lis=[]
title_lis=[]
AssignedTo_lis=[]
state_lis=[]
tags_lis=[]


# a=az("boards query --id 0f54d996-3291-4d92-bf44-aaa86ddbddd7")
# print(a)
 
Input_Id=input("Enter query id: ")
AzResult = namedtuple('AzResult', ['exit_code', 'result_dict', 'log'])
exit_code, result_dict, logs = az(f"boards query --id {Input_Id}")    

if exit_code == 0:
    for item in result_dict:
        AssignedTo_lis.append(item["fields"]["System.AssignedTo"]["displayName"])
        id_lis.append(item["fields"]["System.Id"])
        state_lis.append(item["fields"]["System.State"])
        #tags_lis.append(item["fields"]["System.Tags"])
        title_lis.append(item["fields"]["System.Title"])
        WorkItemType_lis.append(item["fields"]["System.WorkItemType"])
else:
    print(logs)

data={'ID':id_lis, 'Work Item Type':WorkItemType_lis, 'Title':title_lis, 'Assigned To':AssignedTo_lis, 'State':state_lis}
query_result=pd.DataFrame(data)
print(tabulate(query_result, headers='keys', tablefmt='psql'))

