import json
import requests
from datetime import datetime


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

    filterData(url_, data)
    
    return data

def filterData(url_, data):
  
  #Finding date since last issue opened
  date_raw = (data['data']['repository']['issueLastOpened']['nodes'])[0]['createdAt']
  datetime_now = datetime.now()
  datetime_raw = datetime.strptime(date_raw, '%Y-%m-%dT%H:%M:%SZ')
  days_last_issue = datetime_now - datetime_raw
  weeks_last_issue = (days_last_issue.days) / 7
  
  #Checking if README exists
  readme = (data['data']['repository']['object']['text']) 
  if not readme:
    readme_exist = False
  else: 
    readme_exist = True

  #Grabbing other metrics
  doc_exist = (data['data']['repository']['hasWikiEnabled'])
  issues_closed = (data['data']['repository']['issuesClosed']['totalCount'])
  issues_total = issues_closed + (data['data']['repository']['issuesOpen']['totalCount'])
  num_contribute = (data['data']['repository']['assignableUsers']['totalCount'])

  license_correct = 1
  find_license(readme)
  
  print('Has README: ' + str(readme_exist))
  print('Has good documentation: ' + str(doc_exist))
  print('Issues closed: ' + str(issues_closed))
  print('Total issues: ' + str(issues_total))
  print('Number of assignable users: ' + str(num_contribute))
  print('Weeks since last opened issue: ' + str(weeks_last_issue))

  data_list = [url_, readme_exist, doc_exist, issues_closed, issues_total, num_contribute, weeks_last_issue, license_correct]

  return data_list

def find_license(readme):
  #print('Look for license')
  #print(readme)
  index = readme.find('MIT')
  print('License found at index: ' + str(index))


######################################################################

if __name__ == '__main__':
    call_graphQL('https://github.com/cloudinary/cloudinary_npm', "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")

