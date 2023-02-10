import requests
import json

#Input: url = str, api_token = str
#Output: data = str
def call_rest(url, api_token):

    #User = input("Enter name of user: ")
    #url = f"https://api.github.com/user"
    headers = {'Authorization': 'token ' + api_token}
    # for issues

    # output = requests.get(url,data=json.dumps(data))
    # url,readme_exist,doc_exist,issues_closed,issues_total,num_contribute,weeks_last_issue,license_correct
    try:
        # get all issues
        url_issues = url + "/issues"
        query_issues = {"state" : "all"}
        output_issues = requests.get(url_issues, headers=headers, params=query_issues) #data=json.dumps(query)
        data_issues = output_issues.json()
        # get total amount of issues
        issues_total = len(data_issues)

        # find date of last issue and get weeks since, also get closed issues
        issues_closed = 0
        weeks_last_issue = -1
        for issue in data_issues:
            # increment closed issues
            if issue['state'] == 'closed':
                issues_closed += 1
            # find weeks since last issue, date format: 'created_at': '2020-04-20T22:16:33Z'
            weeks_this_issue = abs(datetime.now() - (datetime.strptime(issue['created_at'], '%y/%m/%dT%H:%M:%SZ'))).days//7
            # take care of initial value
            if weeks_last_issue == -1:
                weeks_last_issue = weeks_this_issue
            # if a issue is found that is closer to today, set that as new week since last issue
            else:
                if weeks_this_issue < weeks_last_issue:
                    weeks_last_issue = weeks_this_issue


        # get license
        url_license = url + "/license"
        query_license = {"license" : "LICENSE"} # incorrect?
        output_license = requests.get(url_license, headers=headers, params=query_license)
        data_license = output_license.json()
        if data_license['license'] == "GNU...":
            license_correct = True
        else:
            license_correct = False

        # get readme
        url_readme = url + "/readme"
        query_readme = {"readme" : "README"} # incorrect
        output_readme = requests.get(url_readme, headers=headers, params=query_readme) 
        data_readme = output_readme.json()
        if data_license['readme']:
            readme_exist = True
        else:
            readme_exist = False

        # get contributors
        url_contributors = url + "/contributors"
        query_contributors = {"contributors" : "CONTRIBUTORS"} # incorrect
        output_contributors = requests.get(url_contributors, headers=headers, params=query_contributors)
        data_contributors = output_contributors.json()
        num_contribute = len(data_contributors['contributors'])


        #print(output)
        return [url, readme_exist, doc_exist, issues_closed, issues_total, num_contribute, weeks_last_issue, license_correct]
    except:
        return []