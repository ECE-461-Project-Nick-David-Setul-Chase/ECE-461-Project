import requests
from datetime import datetime 

# Input: url = str, api_token = str
# Output: data = [url,readme_exist,doc_exist,issues_closed,issues_total,num_contribute,weeks_last_issue,license_correct]
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

    try:
        # calculate total issues, closed issues, and weeks since last issue
        # get all issues
        url_issues = "https://api.github.com/search/issues?q=is:issue%20repo:" + user + "/" + repo
        output_issues = requests.get(url_issues, headers=headers)
        data_issues = output_issues.json()
        #print(data_issues)

        if data_issues['incomplete_results']:
            issues_total = 0
            issues_closed = 0
            weeks_last_issue = 0
        else:
            # get total amount of issues
            issues_total = data_issues["total_count"]
            # find date of last issue and get weeks since, also get closed issues
            issues_closed = 0
            #issues_open = 0
            weeks_last_issue = -1
            for issue in data_issues["items"]:
                #print(issue)
                # find closed issues
                if issue['state'] == "closed":
                    issues_closed += 1
                #elif issue['state'] == 'open':
                    #issues_open += 1
                    
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
            #issues_total = issues_open + issues_closed


        # get license DOES NOT WORK
        url_license = rest_url + "/license"
        output_license = requests.get(url_license, headers=headers)
        data_license = output_license.json()
        #print(data_license)
        try:
            # if not found
            if data_license['message']:
                pass
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
                pass
            readme_exist = False
        except:
            if data_readme['name'] == 'README.md':
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
                pass
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
                pass
            doc_exist = False
        except:
            if data_wiki['wiki']:
                doc_exist = True
            else:
                doc_exist = False

        return [readme_exist, doc_exist, issues_closed, issues_total, num_contribute, weeks_last_issue, license_correct]

    except Exception as e:
        #print(e)
        return []
