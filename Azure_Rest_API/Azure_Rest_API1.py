import requests
import base64
import html
import re
import json
import sys
import pandas as pd
from tabulate import tabulate

#Access_Token=  lhddzor2rlrkjwuzltj3pfhpcnn6mecfuqlja5o7ypz26ouxtcca
#Query_Id=  ef3c6390-5496-4acc-80cb-70cc35faeec8
WorkItemType_List=[]
Id_List=[]
AssignedTo_List=[]
Title_List=[]
State_List=[]


def generate_headers():
    if(len(sys.argv)==3):
        Access_Token=sys.argv[1]
    authorization = str(base64.b64encode(bytes(':'+Access_Token, 'ascii')), 'ascii')
    header = { 'Accept': 'application/json', 'Authorization': 'Basic '+authorization }
    return header


def QueryIdStoryTickets_Url():
    if(len(sys.argv)==3):
        query_id=sys.argv[2]
    #response = requests.get(url="https://dev.azure.com/EntropikTechnologies/4ff7c5c1-8f1e-4edc-a70e-4b6bcae4c3dc/_apis/wit/queries/c380204f-7a0c-41d9-b907-b636ce4a540b?api-version=5.1", headers=headers)
    response = requests.get(url=f"https://dev.azure.com/EntropikTechnologies/4ff7c5c1-8f1e-4edc-a70e-4b6bcae4c3dc/_apis/wit/wiql/{query_id}?api-version=5.1", headers=header)
    assert response.status_code==200, 'Error'
    resp=response.json()
    return resp["workItems"]


def Ticket_Details_Fetch():
    BE_FE_RepoBranch_dict={}
    for items in work_items:
        response=requests.get(url=f"{items['url']}", headers=header)
        assert response.status_code==200, 'Error'
        resp=response.json()
        Id_List.append(resp['id'])
        WorkItemType_List.append(resp["fields"]["System.WorkItemType"])
        AssignedTo_List.append(resp["fields"]["System.AssignedTo"]["displayName"])
        State_List.append(resp["fields"]["System.State"])
        Title_List.append(resp["fields"]["System.Title"])
        key_list=list(resp["fields"].keys())
        BE_FE_RepoBranch_dict[resp['id']]={}
        for keys in key_list:
            if(keys=="Custom.BEReposBranch" or keys=="Custom.FEReposBranch"):
                if(keys=="Custom.BEReposBranch"):
                    a=html.unescape(resp["fields"]["Custom.BEReposBranch"])
                    regex=re.compile(r'<[^>]+>')
                    regex=regex.sub('', a)
                    BE_FE_RepoBranch_dict[resp['id']]['BE']=regex
                if(keys=="Custom.FEReposBranch"):
                    a=html.unescape(resp["fields"]["Custom.FEReposBranch"])
                    regex=re.compile(r'<[^>]+>')
                    regex=regex.sub('', a)
                    BE_FE_RepoBranch_dict[resp['id']]['FE']=regex
    data={'ID':Id_List, 'Work Item Type':WorkItemType_List, 'Title':Title_List, 'Assigned To':AssignedTo_List, 'State':State_List}
    query_result=pd.DataFrame(data)
    print(tabulate(query_result, headers='keys', tablefmt='psql'))
    print()
    BE_FE_RepoBranch_json=json.dumps(BE_FE_RepoBranch_dict, indent = 4)
    print(BE_FE_RepoBranch_json)


header=generate_headers()
work_items=QueryIdStoryTickets_Url()
Ticket_Details_Fetch()



