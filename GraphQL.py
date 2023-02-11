import json
import requests
from datetime import datetime

#Arguments: Source URL, API token
#Returns: Dictionary starting with 'data' key
def call_graphQL(url_, api_token):

    url_graphQL = 'https://api.github.com/graphql'
    #https://github.com/
    #https://github.com/
    
    #URL format: https://github.com/user/repo

    #Grabbing everything past https://github.com/
    url_useful = url_[19:]

    #Find index of start of repo name
    repo_index = url_useful.find('/')
    user = url_useful[0 : repo_index]
    repo = url_useful[(repo_index + 1) :]

    #NEED TO ADD LICENSE TO THIS JUST IN CASEEEEEEEEEEEEEE
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
    
    #Check for error
    if(response.status_code >= 400):
        filteredData = []
    else:
        data = json.loads(response.text)
        filteredData = filterData(data)
    
    return filteredData

def filterData(data):
  
    #Finding date since last issue opened
    date_raw = (data['data']['repository']['issueLastOpened']['nodes'])[0]['createdAt']
    datetime_now = datetime.now()
    datetime_raw = datetime.strptime(date_raw, '%Y-%m-%dT%H:%M:%SZ')
    days_last_issue = datetime_now - datetime_raw
    weeks_last_issue = (days_last_issue.days) / 7

    #Checking if README exists
    if (data['data']['repository']['object']) is None:
        readme_exist = False
        readme = ""
    else:
        readme = (data['data']['repository']['object']['text']) 
        readme_exist = True

    #Grabbing other metrics
    doc_exist = (data['data']['repository']['hasWikiEnabled'])
    issues_closed = (data['data']['repository']['issuesClosed']['totalCount'])
    issues_total = issues_closed + (data['data']['repository']['issuesOpen']['totalCount'])
    num_contribute = (data['data']['repository']['assignableUsers']['totalCount'])

    license_correct_readme = True
    find_license(readme)

    data_list = [readme_exist, doc_exist, issues_closed, issues_total, num_contribute, weeks_last_issue, license_correct_readme]

    return data_list

def find_license(readme):
    #print('Look for license')
    #print(readme)
    
    index = readme.find('MIT')
    print('License found at index: ' + str(index))


######################################################################



