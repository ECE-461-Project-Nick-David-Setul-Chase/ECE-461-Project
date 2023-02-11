import json
import requests
from datetime import datetime

GNU_GPL = ["GPL-3.0-only", "GPL-3.0-or-later", "GPL-2.0-only", "GPL-2.0-or-later", "LGPL-2.1-only", "LGPL-2.1-or-later", "LGPL-3.0-only", "LGPL-3.0-or-later", \
    "AGPL-3.0", "Apache-2.0", "Artistic-2.0", "ClArtistic", "BSL-1.0", "CECILL-2.0", "eCos-2.0", "ECL-2.0", "EFL-2.0", "EUDatagrid", "BSD-2-Clause-FreeBSD", \
        "FTL", "HPND", "iMatix", "Imlib2", "IJG", "Intel", "ISC", "MPL-2.0", "NCSA", "Python-2.0.1", "Python-2.1.1", "Ruby", "SGI-B-2.0", "StandardML-NJ", \
            "SMLNJ", "Unicode-DFS-2015", "Unicode-DFS-2016", "UPL-1.0", "Unlicense", "Vim", "WTFPL", "X11", "MIT", "XFree86-1.1", "Zlib", "ZPL-2.0", "ZPL-2.1"]

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
            licenseInfo{
                key
            }
            hasWikiEnabled
        }
    }'''

    json_ = { 'query' : query_ } 
    headers_ = {'Authorization': 'token %s' % api_token}
    response = requests.post(url=url_graphQL, json=json_, headers=headers_)
    
    #Check for error
    data = json.loads(response.text)
    #print(data)
    if(response.status_code >= 400 or data['data']['repository'] == None):
        filteredData = []
    else:
        #data = json.loads(response.text)
        filteredData = filterData(data)
    
    return filteredData

def filterData(data):
    
    license_correct = 0

    #Finding date since last issue opened

    weeks_last_issue = 0
    if data['data']['repository']['issueLastOpened']['nodes'] != []:
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
        license_correct = find_license(readme)

    #Grabbing other metrics
    doc_exist = (data['data']['repository']['hasWikiEnabled'])
    issues_closed = (data['data']['repository']['issuesClosed']['totalCount'])
    issues_total = issues_closed + (data['data']['repository']['issuesOpen']['totalCount'])
    num_contribute = (data['data']['repository']['assignableUsers']['totalCount'])
    
    if (data['data']['repository']['licenseInfo']) is not None:
        print("License: " + str(data['data']['repository']['licenseInfo']['key']))
        license_correct = find_license(data['data']['repository']['licenseInfo']['key']) or license_correct

    data_list = [readme_exist, doc_exist, issues_closed, issues_total, num_contribute, weeks_last_issue, license_correct]

    return data_list

def find_license(string):
    
    for license in GNU_GPL:
        indexLow = string.find(license.lower())
        indexUp = string.find(license.upper())
        
        if indexLow != -1 or indexUp != -1: 
            #print('License found: ' + license)
            return True
    
    return False
        


######################################################################



