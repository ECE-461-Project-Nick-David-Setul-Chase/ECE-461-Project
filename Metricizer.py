import sys
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = "/usr/lib/git-core" 

import git
from git.repo.base import Repo

#this is gitpython
# From .env import load_.env load_dotenv()
from GraphQL import call_graphQL
from REST import call_rest
# sys.path.append('../')

OTHER = 0
GITHUB = 1
NPMJS = 2

API_ERR = -3
OTHER_ERR = -2
NPMJS_ERR = -1

INFO = 1
DEBUG = 2

#TO DO: Clone repo, web scrap

def metricizer(inputfile):

    success = 0

    #if len(sys.argv) != 2:
    #    print("ERROR. Proper use: python3 Metricizer/Metricizer url-file.txt")
    #    exit(1)
    
    #Grab API token
    api_token = os.environ.get("GITHUB_TOKEN") 
    log_level = int(os.environ.get("LOG_LEVEL")) 
    log_file = os.environ.get("LOG_FILE") 

    #Creating metric output file
    output_metric = open('output_metric.txt', 'w')
    log_output = open(log_file, 'w')

    writeLog(log_output, log_level, str(datetime.now) + " - " + "System Start", INFO)

    #Open input file
    file_ptr = open(sys.argv[1]) #THE REAL DEAL

    #Read line by line in URL input file
    writeLog(log_output, log_level, str(datetime.now) + " - " + "Processing URL Inputs", INFO)
    for url in file_ptr:

        url = url.strip()

        writeLog(log_output, log_level, str(datetime.now) + " - " + "Analyzing " + url, DEBUG)
        
        print(str(url) + "...")
        
        domain = getDomain(url)
        
        if (domain == OTHER):
            #print("Unsupported domain detected.\nModules must be supported on one of the following domains:\n  - github.com\n  - npmjs.com")
            writeOutput(output_metric, [url, OTHER_ERR, OTHER_ERR, OTHER_ERR, OTHER_ERR, OTHER_ERR, OTHER_ERR, OTHER_ERR])
            writeLog(log_output, log_level, str(datetime.now) + " - " + "Unsupported URL Input", DEBUG)
            pass
        
        if (domain == NPMJS):
            github_found = npmjs_scrap(url)
            if not github_found:
                #print("Unsupported npmjs.com module.\nNo corresponding github.com module.")
                writeOutput(output_metric, [url, NPMJS_ERR, NPMJS_ERR, NPMJS_ERR, NPMJS_ERR, NPMJS_ERR, NPMJS_ERR, NPMJS_ERR])
                writeLog(log_output, log_level, str(datetime.now) + " - " + "Unsupported URL Input", DEBUG)
                pass
            else: 
                domain = GITHUB
                url = github_found
                #print(url)

        if (domain == GITHUB):
            #print("github.com module detected/found.")

            #Grab list from APIs --- [readme_exist, doc_exist, issues_closed, issues_total, num_contribute, weeks_last_issue, license_correct]
            writeLog(log_output, log_level, str(datetime.now) + " - " + "Calling GraphQL API & REST API", DEBUG)
            gql_info = call_graphQL(url, api_token)
            rest_info = call_rest(url, api_token)

            if not gql_info:
                #print("API response failed. Please check token and WIFI ccccconnection.")
                data = [API_ERR, API_ERR, API_ERR, API_ERR, API_ERR, API_ERR, API_ERR, API_ERR]
                writeOutput(output_metric, data)
                writeLog(log_output, log_level, str(datetime.now) + " - " + "Unsuccessful GraphQL API Call", DEBUG)
                return 1
            if not rest_info:
                #print("API response failed. Please check token and WIFI ccccconnection.")
                data = [API_ERR, API_ERR, API_ERR, API_ERR, API_ERR, API_ERR, API_ERR, API_ERR]
                writeOutput(output_metric, data)
                writeLog(log_output, log_level, str(datetime.now) + " - " + "Unsuccessful GraphQL API Call", DEBUG)
                return 1

            path = createDir(url)
            Repo.clone_from(url, path)

            print("_________")
            print(gql_info)
            print(rest_info)
            print("_________")
            
            #Find metric params
            readme_exist = int(gql_info[0])
            doc_exist = int(gql_info[1])
            issues_closed = gql_info[2]
            issues_total1 = gql_info[3]
            issues_total2 = rest_info[3]
            #print("GraphQL issues: " + str(issues_total1) + " REST issues: " + str(issues_total2))
            num_contribute = gql_info[4]
            weeks_last_issue = gql_info[5]
            license_correct = int(gql_info[6])

            data = [url, readme_exist, doc_exist, issues_closed, issues_total1, num_contribute, weeks_last_issue, license_correct]

            writeLog(log_output, log_level, str(datetime.now) + " - " + "Response Data Saved", DEBUG)

            writeOutput(output_metric, data) 

    writeLog(log_output, log_level, str(datetime.now) + " - " + "All Data Written", INFO)
    writeLog(log_output, log_level, str(datetime.now) + " - " + "Calculating Metrics & Total Score", INFO)
    
    #Closing all files
    file_ptr.close()
    output_metric.close()
    log_output.close()

    return success 


#Determine module source domain
def getDomain(url):
    domain = OTHER
    if(url.find("https://github.com") != -1):
        domain = GITHUB
    elif(url.find("https://www.npmjs.com") != -1):
        domain = NPMJS
    return domain


#Write metrics to metric output
#Format: url,readme_exist,doc_exist,issues_closed,issues_total,num_contribute,weeks_last_issue,license_correct
#Example: https://github.com/user/repo,1,1,45,64,5,2,1
def writeOutput(output_metric, data):
    output_metric.write(str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "," + str(data[3]) + "," + str(data[4]) + "," + \
        str(data[5]) + "," + str(data[6]) + "," + str(data[7]) + "\n")


def writeLog(file_ptr, log_level, string, access_level):
    if(access_level <= log_level):
        file_ptr.write(string)


#Web scrapping NPMJS to find GitHub repo
def npmjs_scrap(url):
    req = requests.get(url)
    soupTime = BeautifulSoup(req.text, "html.parser")
    if(soupTime.find("a", {"aria-labelledby":"repository repository-link"})) is None:
        return("")
    else:
        return(str(soupTime.find("a", {"aria-labelledby":"repository repository-link"})['href']))

def createDir(url_):
    #Grabbing repo name
    url_useful = url_[19:]
    repo_index = url_useful.find('/')
    repo = (url_useful[(repo_index + 1) :]).strip()

    #Create new directory
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, repo)
    os.mkdir(path)

    return path


#####################################################
if __name__ == '__main__':
    metricizer("testurls.txt")