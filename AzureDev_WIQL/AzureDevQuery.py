import requests
import base64
from AzureDevQuery2 import *
import pandas as pd
from tabulate import tabulate

id_lis=[]
pat = 'lhddzor2rlrkjwuzltj3pfhpcnn6mecfuqlja5o7ypz26ouxtcca'
authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')

headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic '+authorization
}

#response = requests.get(url="https://dev.azure.com/EntropikTechnologies/4ff7c5c1-8f1e-4edc-a70e-4b6bcae4c3dc/_apis/wit/queries/c380204f-7a0c-41d9-b907-b636ce4a540b?api-version=5.1", headers=headers)
response = requests.get(url="https://dev.azure.com/EntropikTechnologies/4ff7c5c1-8f1e-4edc-a70e-4b6bcae4c3dc/_apis/wit/wiql/c380204f-7a0c-41d9-b907-b636ce4a540b?api-version=5.1", headers=headers)

res=response.json()

work_items=res["workItems"]

for i in range(0, len(work_items)):
    id_lis.append(work_items[i]["id"])


for ids in id_lis:
    q=f"SELECT [System.Title] FROM workitems WHERE [System.Id] = {ids}"
    get_TC_from_query(q)

data={'ID':Id_Lis, 'Work Item Type':WorkItemType_Lis, 'Title':Title_Lis, 'Assigned To':AssignedTo_Lis, 'State':State_Lis}
query_result=pd.DataFrame(data)
print(tabulate(query_result, headers='keys', tablefmt='psql'))







#lhddzor2rlrkjwuzltj3pfhpcnn6mecfuqlja5o7ypz26ouxtcca