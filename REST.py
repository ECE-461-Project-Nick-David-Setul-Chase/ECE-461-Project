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
            weeks_this_issue = abs(datetime.now() - (datetime.strptime(issue['created_at'], '%m/%d/%yT%H:%M:%SZ'))).days//7
            # take care of initial value
            if weeks_last_issue == -1:
                weeks_last_issue = weeks_this_issue
            # if a issue is found that is closer to today, set that as new week since last issue
            else:
                if weeks_this_issue < weeks_last_issue:
                    weeks_last_issue = weeks_this_issue

        #print(output)
        return [url, readme_exist, doc_exist, issues_closed, issues_total, num_contribute, weeks_last_issue, license_correct];
    except:
        return []