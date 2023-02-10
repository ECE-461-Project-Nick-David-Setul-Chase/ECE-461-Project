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

def filterData(data):
  
  readme = (data['data']['repository']['object']['text']) 
  if not readme:
    readme_exist = False
  else: 
    readme_exist = True

  doc_exist = (data['data']['repository']['hasWikiEnabled'])
  issues_closed = (data['data']['repository']['issuesClosed']['totalCount'])
  issues_total = issues_closed + (data['data']['repository']['issuesOpen']['totalCount'])
  num_contribute = (data['data']['repository']['assignableUsers']['totalCount'])
  weeks_last_issue = 2
  license_correct = 1
  #ISO-8601 encoded UTC date string.
  
  print('Has README: ' + str(readme_exist))
  print('Has good documentation: ' + str(doc_exist))
  print('Issues closed: ' + str(issues_closed))
  print('Total issues: ' + str(issues_total))
  print('Number of assignable users: ' + str(num_contribute))

