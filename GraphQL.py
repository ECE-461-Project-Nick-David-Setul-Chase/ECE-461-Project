import json
import requests

#Arguments: Source URL, API token
#Returns: Dictionary starting with 'data' key
def call_graphQL(url_, api_token):

    url_graphQL = 'https://api.github.com/graphql'
    
    #URL format: https://github.com/user/repo

    #Grabbing everything past https://github.com/
    url_useful = url_[19:]

    #Find index of start of repo name
    repo_index = url_useful.find('/')
    user = url_useful[0 : repo_index]
    repo = url_useful[(repo_index + 1) :]

    #Query to get needed data from API
    query_ = '''
    { 
        repository(owner:"''' + user + '''", name:"''' + repo + '''") {
            issuesOpen: issues(states:OPEN){
                totalCount
            }
            issuesClosed: issues(states:CLOSED){
                totalCount
            }
            issueLastOpened: issues(states:OPEN, orderBy:{field: CREATED_AT, direction: DESC}, first:1){
                nodes{
                    createdAt
                }
            }
            assignableUsers{
                totalCount
            }
            object(expression: "master:README.md") {
            ... on Blob {
                text
                }
            }
            hasWikiEnabled
        }
    }'''

    json_ = { 'query' : query_ } 
    headers_ = {'Authorization': 'token %s' % api_token}
    response = requests.post(url=url_graphQL, json=json_, headers=headers_)
    data = json.loads(response.text)

    return data

