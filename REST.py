import requests
import json

#Input: url = str, api_token = str
#Output: data = str
def call_rest(url, api_token):
    #User = input("Enter name of user: ")
    url = "https://api.github.com/user"
    headers = {'Authorization': 'token ' + api_token}

    data = {"type" : "all", "sort" : "full_name", "direction" : "asc"}
    # output = requests.get(url,data=json.dumps(data))
    output = requests.get(url, headers=headers,data=json.dumps(data))
    output = json.loads(output.text)
    print(output)