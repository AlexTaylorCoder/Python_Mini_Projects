import requests
import datetime as dt

TOKEN = "bananabanana123"
USERNAME = "alexcoder515"
pixela_endpoint = "https://pixe.la/v1/users"
graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"
point_endpoint = f"{graph_endpoint}/graph1"

def find_date():
    return dt.datetime.now().strftime("%Y%m%d")


delete_point_by_day = f"{point_endpoint}/{find_date()}"
update_point_by_day = f"{point_endpoint}/{find_date()}"



user_params = {
    "token": TOKEN,
    "username":USERNAME,
    "agreeTermsOfService":"yes",
    "notMinor":"yes"
}

graph_params = {
    "id": "graph1",
    "name": "running",
    "unit": "Km",
    "type": "float",
    "color": "sora"
}

#strftime allows for custom formatting of date
point_params = {
    "date": find_date(),
    "quantity": "2",
    "optionalData":'{"text":"It worked!"}'
}

update_params = {
    "quantity":"4"
}

headers = {
    "X-USER-TOKEN":TOKEN
}

# Create account
# requests.post(url=pixela_endpoint,json=user_params)

# graph_data = requests.post(url=graph_endpoint,json=graph_params,headers=headers)

point_data = requests.post(url=point_endpoint,json=point_params,headers=headers)
# delete_point = requests.delete(url=delete_point_by_day,headers=headers)
update_point = requests.put(url=update_point_by_day,headers=headers,json=update_params)

# print(delete_point.json())
print(update_point.json())



