# import requests
# import json

# #Input: url = str, api_token = str
# #Output: data = dictionary
# def call_graphQL(url_, api_token):

#     #Defines what we want
#     json_ = { 'query' : '{ viewer { repositories(first: 30) { totalCount pageInfo { hasNextPage endCursor } edges { node { name } } } } }' }
#     #Data sent to API
#     headers = {'Authorization': 'token %s' % api_token}
#     #Collecting data
#     data_dict = requests.post(url=url_, json=json_, headers=headers)

#     return data_dict.text


# #Number of comments
# #Does README exist?
# #Does documentation exist?
# #Number of contributors
# #Number of issues
# #GNU LGPL 2.1 compatible/check licensing

# def idk():
#     response = requests.get(url)
#     if(response != 200):
#         print("GraphQL.py: Query Request Error Code {response}")





import json
import requests
 

# https://stackoverflow.com/questions/47458143/how-to-download-github-repositories-via-graphql-api-search


url_ = 'https://api.github.com/graphql'
# json_ = { 'query' : '{ viewer { name repositories(first: 3) { totalCount pageInfo { hasNextPage endCursor } edges { node { name } } } } }' }

# json_ = { 'query' : '{ repository(owner: "google", name: "gson") { defaultBranchRef { target { ... on Commit { tarballUrl zipballUrl } } } } }' }
# json_ = { 'query' : '{ repository(owner: "cloudinary", name: "cloudinary_npm") { defaultBranchRef { target { ... on Commit { tarballUrl zipballUrl } } } } }' }
json_ = { 'query' : '{ repository(owner: "cloudinary", name: "cloudinary_npm") { updatedAt } }' }
# json_ = { 'UniformResourceLocatable' : ' { User }' }
# json_ = { repository(url: url_) { } }
# json_ = { 'repository(url: {})'.format(url_) : '{ viewer { name repositories(first: 3) { totalCount pageInfo { hasNextPage endCursor } edges { node { name } } } } }' }
api_token = "GITHUB KEY HERE"
headers = {'Authorization': 'token %s' % api_token}

r = requests.post(url=url_, json=json_, headers=headers)
print (r.text)

