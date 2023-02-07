import json
import requests

def call_graphQL(url):

    #url_ = 'https://api.github.com/graphql'

    json_ = { 'query' : '{ repository(owner: "cloudinary", name: "cloudinary_npm") { updatedAt } }' }
    api_token = "GITHUB KEY HERE"
    headers = {'Authorization': 'token %s' % api_token}

    r = requests.post(url=url_, json=json_, headers=headers)
    print (r.text)

