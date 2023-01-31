import requests
import base64
import pandas as pd
from tabulate import tabulate

WorkItemType_Lis=[]
Id_Lis=[]
AssignedTo_Lis=[]
Title_Lis=[]
State_Lis=[]

pat = 'lhddzor2rlrkjwuzltj3pfhpcnn6mecfuqlja5o7ypz26ouxtcca'
authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')

headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic '+authorization
}

query_id=input("Enter the query id: ")

#response = requests.get(url="https://dev.azure.com/EntropikTechnologies/4ff7c5c1-8f1e-4edc-a70e-4b6bcae4c3dc/_apis/wit/queries/c380204f-7a0c-41d9-b907-b636ce4a540b?api-version=5.1", headers=headers)
response1 = requests.get(url=f"https://dev.azure.com/EntropikTechnologies/4ff7c5c1-8f1e-4edc-a70e-4b6bcae4c3dc/_apis/wit/wiql/{query_id}?api-version=5.1", headers=headers)

res1=response1.json()

work_items=res1["workItems"]

for items in work_items:
    response2=requests.get(url=f"{items['url']}", headers=headers)
    res2=response2.json()
    Id_Lis.append(res2['id'])
    WorkItemType_Lis.append(res2["fields"]["System.WorkItemType"])
    AssignedTo_Lis.append(res2["fields"]["System.AssignedTo"]["displayName"])
    State_Lis.append(res2["fields"]["System.State"])
    Title_Lis.append(res2["fields"]["System.Title"])

data={'ID':Id_Lis, 'Work Item Type':WorkItemType_Lis, 'Title':Title_Lis, 'Assigned To':AssignedTo_Lis, 'State':State_Lis}
query_result=pd.DataFrame(data)
print(tabulate(query_result, headers='keys', tablefmt='psql'))


