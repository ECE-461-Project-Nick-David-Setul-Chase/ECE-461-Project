import requests
import json

#Input: url = str, api_token = str
#Output: data = str
def call_graphQL(url, api_token):
    #url = 'https://api.github.com/graphql'
    #api_token = "PUT TOKEN HERE"
    json = { 'query' : '{ viewer { repositories(first: 30) { totalCount pageInfo { hasNextPage endCursor } edges { node { name } } } } }' }
    headers = {'Authorization': 'token %s' % api_token}
    r = requests.post(url=url, json=json, headers=headers)
    print (r.text)

    return r