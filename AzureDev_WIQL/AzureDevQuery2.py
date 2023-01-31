from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v5_1.work_item_tracking.models import Wiql


token = "lhddzor2rlrkjwuzltj3pfhpcnn6mecfuqlja5o7ypz26ouxtcca"
team_instance = "https://dev.azure.com/EntropikTechnologies"

credentials = BasicAuthentication("", token)
connection = Connection(base_url=team_instance, creds=credentials)

WorkItemType_Lis=[]
Id_Lis=[]
AssignedTo_Lis=[]
Title_Lis=[]
State_Lis=[]


def print_work_items(work_items):
    for work_item in work_items:
        # print(
        #     "{0} {1} {2}: {3}".format(
        #         work_item.fields["System.WorkItemType"],
        #         work_item.id,
        #         work_item.fields["System.AssignedTo"]['displayName'],
        #         work_item.fields["System.Title"],
        #     )

        # )
        WorkItemType_Lis.append(work_item.fields["System.WorkItemType"])
        Id_Lis.append(work_item.id)
        AssignedTo_Lis.append(work_item.fields["System.AssignedTo"]['displayName'])
        Title_Lis.append(work_item.fields["System.Title"])
        State_Lis.append(work_item.fields["System.State"])


wit_client = connection.clients.get_work_item_tracking_client()


def get_TC_from_query(query):
    query_wiql = Wiql(query=query)
    results = wit_client.query_by_wiql(query_wiql).work_items
    # WIQL query gives a WorkItemReference => we get the corresponding WorkItem from id
    work_items = (wit_client.get_work_item(int(result.id)) for result in results)
    print_work_items(work_items)


#q="SELECT [System.Id] FROM workitems WHERE [System.State] = 'Qa In Progress' AND [System.WorkItemType]='Story'"
# q="SELECT [System.Id] FROM workitems WHERE [System.QueryId] = 'c380204f-7a0c-41d9-b907-b636ce4a540b'"
