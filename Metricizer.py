import sys
import os
import requests
from bs4 import BeautifulSoup
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = os.getcwd() 
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

#TO DO: Clone repo, web scrap

def metricizer(inputfile):

    success = 0
    
    #print(sys.argv)

    #if len(sys.argv) != 2:
    #    print("ERROR. Proper use: python3 Metricizer/Metricizer url-file.txt")
    #    exit(1)
    # for line in sys.stdin:
    #     print(line)
    
    #Grab API token
    #api_token = os.environ.get("GITHUB_TOKEN") #THE REAL DEAL
    api_token = "fill in" #FOR TESTING ONLY

    #Creating metric output file
    output_metric = open('output_metric.txt', 'w')

    #Open input file
    #file_ptr = open(sys.argv[1]) #THE REAL DEAL
    file_ptr = open(inputfile) #FOR TESTING ONLY

    #Read line by line in URL input file
    for url in file_ptr:
        
        #path = createDir(url)
        #print(path)

        url = url.strip()
        
        domain = getDomain(url)
        
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
                print(url)

        if (domain == GITHUB):
            print("github.com module detected/found.")

            #Grab list from APIs --- [readme_exist, doc_exist, issues_closed, issues_total, num_contribute, weeks_last_issue, license_correct]
            gql_info = call_graphQL(url, api_token)
            rest_info = call_rest(url, api_token)

            if not gql_info:
                print("API response failed. Please check token and WIFI connection.")
                data = [API_ERR, API_ERR, API_ERR, API_ERR, API_ERR, API_ERR, API_ERR, API_ERR]
                writeOutput(output_metric, data)
                return 1

            #Repo.clone_from(url, path)
            
            #Find metric params
            readme_exist = int(gql_info[0])
            doc_exist = int(gql_info[1])
            issues_closed = gql_info[2]
            issues_total1 = gql_info[3]
            issues_total2 = rest_info[3]
            print("GraphQL issues: " + str(issues_total1) + " REST issues: " + str(issues_total2))
            num_contribute = gql_info[4]
            weeks_last_issue = gql_info[5]
            license_correct = int(gql_info[6])

            data = [url, readme_exist, doc_exist, issues_closed, issues_total1, num_contribute, weeks_last_issue, license_correct]

            writeOutput(output_metric, data) 


    #Closing all files
    file_ptr.close()
    output_metric.close()

    return 0 


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


#Web scrapping NPMJS to find GitHub repo
def npmjs_scrap(url):
    req = requests.get(url)
    soupTime = BeautifulSoup(req.text, "html.parser")
    row = soupTime.find("a", {"aria-labelledby":"repository repository-link"})['href']
    if row is None:
        return("")
    else: return(row)
    

def createDir(url_):
    #Grabbing repo name
    url_useful = url_[19:]
    repo_index = url_useful.find('/')
    repo = (url_useful[(repo_index + 1) :]).strip()

    #Create new directory
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, repo)
    print(path)
    os.mkdir(path)

    return path


#####################################################
if __name__ == '__main__':
    metricizer("testurls.txt")