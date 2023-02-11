import sys
import os
import requests
from bs4 import BeautifulSoup
# From .env import load_.env load_dotenv()
from GraphQL import call_graphQL
from REST import call_rest
# sys.path.append('../')

OTHER = 0
GITHUB = 1
NPMJS = 2

OTHER_ERR = -2
NPMJS_ERR = -1


#TO DO: Clone repo, web scrap

def metricizer(inputfile):

    #print(sys.argv)

    #if len(sys.argv) != 2:
    #    print("ERROR. Proper use: python3 Metricizer/Metricizer url-file.txt")
    #    exit(1)
    # for line in sys.stdin:
    #     print(line)
    
    #Grab API token
    #api_token = os.environ.get("GITHUB_TOKEN") 
    api_token = "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" #FOR TESTING ONLY

    #Creating metric output file
    output_metric = open('output_metric.txt', 'w')

    #Open input file
    #file_ptr = open(sys.argv[1])
    file_ptr = open(inputfile) #FOR TESTING ONLY

    #Read line by line in URL input file
    for url in file_ptr:
        
        url = url.strip()
        
        domain = getDomain(url)

        print("___________")
        print(url)
        
        if (domain == OTHER):
            print("Unsupported domain detected.\nModules must be supported on one of the following domains:\n  - github.com\n  - npmjs.com")
            writeOutput(output_metric, [url, OTHER_ERR, OTHER_ERR, OTHER_ERR, OTHER_ERR, OTHER_ERR, OTHER_ERR, OTHER_ERR])
            pass
        
        if (domain == NPMJS):
            github_found = npmjs_scrap(url)
            if not github_found:
                print("Unsupported npmjs.com module.\nNo corresponding github.com module.")
                writeOutput(output_metric, [url, NPMJS_ERR, NPMJS_ERR, NPMJS_ERR, NPMJS_ERR, NPMJS_ERR, NPMJS_ERR, NPMJS_ERR])
                pass
            else: 
                domain = GITHUB
                url = github_found

        if (domain == GITHUB):
            print("github.com module detected/found.")

            #Grab list from APIs --- [readme_exist, doc_exist, issues_closed, issues_total, num_contribute, weeks_last_issue, license_correct]
            gql_info = call_graphQL(url, api_token)
            rest_info = call_rest(url, api_token)

            print(gql_info)
            print(rest_info)

            #Find metric params
            readme_exist = int(gql_info[0])
            doc_exist = int(gql_info[1])
            issues_closed = rest_info[2]
            issues_total = rest_info[3]
            num_contribute = gql_info[4]
            weeks_last_issue = gql_info[5]
            license_correct = int(gql_info[6])

            data = [url, readme_exist, doc_exist, issues_closed, issues_total, num_contribute, weeks_last_issue, license_correct]

            writeOutput(output_metric, data) 


    #Closing all files
    file_ptr.close()
    output_metric.close()

#Determine module source domain
def getDomain(url):
    domain = OTHER
    if(url.find("github.com") != -1):
        domain = GITHUB
    elif(url.find("npmjs.com") != -1):
        domain = NPMJS
    return domain

#Write metrics to metric output
#Format: url,readme_exist,doc_exist,issues_closed,issues_total,num_contribute,weeks_last_issue,license_correct
#Example: https://github.com/user/repo,1,1,45,64,5,2,1
def writeOutput(output_metric, data):
    output_metric.write(str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "," + str(data[3]) + "," + str(data[4]) + "," + \
        str(data[5]) + "," + str(data[6]) + "," + str(data[7]) + "\n")


def npmjs_scrap(url):
    req = requests.get(url)
    soupTime = BeautifulSoup(req.text, "html.parser")
    row = soupTime.find("a", {"aria-labelledby":"repository repository-link"})['href']
    if row is None:
        return("")
    else: return(row)
    

#####################################################
if __name__ == '__main__':
    metricizer("testurls.txt")