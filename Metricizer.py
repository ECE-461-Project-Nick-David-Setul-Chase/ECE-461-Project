import sys
import os

# sys.path.append('../')

import GraphQL.py
import REST.py
# From .env import load_.env load_dotenv()

def Main(inputfile):

    print(sys.argv)

    if len(sys.argv) != 2:
        print("ERROR. Proper use: python3 Metricizer/Metricizer url-file.txt")
        exit(1)
    # for line in sys.stdin:
    #     print(line)
    
    #Grab API token
    api_token = os.environ.get("GITHUB_TOKEN") 

    #Creating metric output file
    output_metric = open('output_metric.txt', 'w')

    #Open input file
    file_ptr = open(sys.argv[1])

    #Read line by line in URL input file
    for url in file_ptr:
        #Grab dictionary from graphQL API
        gql_info = call_graphQL(url, api_token)
        
        #Grab dictionary from REST API
        rest_info = call_rest(url, api_token)

        #Find metric params
        readme_exist = true
        doc_exist = true
        issues_closed = 5
        issues_total = 10
        num_contribute = 5
        weeks_last_issue = 2
        license_correct = true

        #Write metrics to metric output
        #Format: url,readme_exist,doc_exist,issues_closed,issues_total,num_contribute,weeks_last_issue,license_correct
        #Example: https://github.com/user/repo,1,1,45,64,5,2,1
        output_metric.write(url + "," + readme_exist + "," + doc_exist + "," + issues_closed + "," + issues_total + "," + num_contribute + "," + weeks_last_issue + "," + license_correct + "\n")

    #Closing all files
    file_ptr.close()
    output_metric.close()

def calc_rampup(info):
    return -999
    pass

def calc_correctness(info):
    return -999
    pass

def calc_busfactor(info):
    return -999
    pass

def calc_responsive_maintainer(info):
    return -999
    pass

def calc_license(info):
    return -999
    pass

        # info = "deleteME"
        # rampup = calc_rampup(info)
        # correctness = calc_correctness(info)
        # busfactor = calc_busfactor(info)
        # responsive_maintainer = calc_responsive_maintainer(info)
        # repo_license = calc_license(info)