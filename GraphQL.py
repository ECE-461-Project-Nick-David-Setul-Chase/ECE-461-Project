import json
import requests

def call_graphQL(url_):

    #URL format: https://github.com/user/repo

    #Grabbing everything past https://github.com/
    url_useful = url_[19:]

    #Find index of start of repo name
    repo_index = url_.find('/')

    user = url_useful[0 : repo_index]
    repo = url_useful[(repo_index + 1) :]

    #json_ = { 'query' : '{ repository(owner: "cloudinary", name: "cloudinary_npm") { updatedAt } }' }

    query_ = '{ repository(owner:"' + user + '", name:"' + repo + '") { issues(states:OPEN) {totalCount}}}'

    json_ = { 'query' : query_ } 
    api_token = "GITHUB KEY HERE"
    headers_ = {'Authorization': 'token %s' % api_token}

    r = requests.post(url=url_, json=json_, headers=headers_)
    print (r.text)

