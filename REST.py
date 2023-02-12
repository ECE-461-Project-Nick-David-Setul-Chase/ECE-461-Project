import requests
import json
from datetime import datetime 

#Input: url = str, api_token = str
#Output: data = str
def call_rest(url, api_token):

    # authorization token
    headers = {'Authorization': 'token ' + api_token}

    # grabbing everything past https://github.com/
    url_useful = url[19:]

    # find index of start of repo name
    repo_index = url_useful.find('/')

    # get user and repo
    user = url_useful[0 : repo_index]
    repo = url_useful[(repo_index + 1) :]

    # create url for rest api
    rest_url = 'https://api.github.com/repos/' + user + '/' + repo

    # output format: url,readme_exist,doc_exist,issues_closed,issues_total,num_contribute,weeks_last_issue,license_correct

    try:
        # calculate total issues, closed issues, and weeks since last issue
        # get all issues
        url_issues = rest_url + "/issues"
        query_issues_closed = {"state" : "closed"}
        output_issues_closed = requests.get(url_issues, headers=headers, params=query_issues_closed)
        query_issues_open = {"state" : "open"}
        output_issues_open = requests.get(url_issues, headers=headers, params=query_issues_open)
        data_issues_closed = output_issues_closed.json()
        data_issues_open = output_issues_open.json()
        #print(data_issues)
        try:
            # if not found
            if data_issues_open['message'] | data_issues_closed['message']:
                issues_total = 0
                issues_closed = 0
                weeks_last_issue = 0
        except:
            # get total amount of issues
            issues_total = len(data_issues_open) + len(data_issues_closed)

            # find date of last issue and get weeks since, also get closed issues
            issues_closed = len(data_issues_closed)
            weeks_last_issue = -1
            for issue in (data_issues_closed + data_issues_open):
                #print(issue)

                # find weeks since last issue, date format: 'created_at': '2020-04-20T22:16:33Z'
                weeks_this_issue = abs(datetime.now() - datetime.fromisoformat(issue['created_at'].replace('Z', ''))).days//7
                # take care of initial value
                if weeks_last_issue == -1:
                    weeks_last_issue = weeks_this_issue
                # if a issue is found that is closer to today, set that as new week since last issue
                else:
                    if weeks_this_issue < weeks_last_issue:
                        weeks_last_issue = weeks_this_issue
            # fail safe if no issues
            if weeks_last_issue == -1:
                weeks_last_issue = 0


        # get license DOES NOT WORK
        url_license = rest_url + "/license"
        output_license = requests.get(url_license, headers=headers)
        data_license = output_license.json()
        #print(data_license)
        try:
            # if not found
            if data_license['message']:
                license_correct = False
        except:
            if data_license['license'] == "GNU...":
                license_correct = True
            else:
                license_correct = False

        # get readme
        url_readme = rest_url + "/readme"
        output_readme = requests.get(url_readme, headers=headers)
        data_readme = output_readme.json()
        #print(data_readme)
        try:
            # if not found
            if data_readme['message']:
                license_correct = False
        except:
            if data_readme['name']:
                readme_exist = True
            else:
                readme_exist = False

        # get contributors
        url_contributors = rest_url + "/contributors"
        output_contributors = requests.get(url_contributors, headers=headers)
        data_contributors = output_contributors.json()
        #print(data_contributors)
        try:
            # if not found
            if data_contributors['message']:
                num_contribute = 0
        except:
            num_contribute = len(data_contributors)

        # get wiki (documentation) DOES NOT WORK
        url_wiki = rest_url + "/wikis"
        output_wiki = requests.get(url_wiki, headers=headers)
        data_wiki = output_wiki.json()
        #print(data_wiki)
        try:
            # if not found
            if data_wiki['message']:
                doc_exist = False
        except:
            if data_wiki['wiki']:
                doc_exist = True
            else:
                doc_exist = False

        return [url, readme_exist, doc_exist, issues_closed, issues_total, num_contribute, weeks_last_issue, license_correct]

    except Exception as e:
        print(e)
        return []
