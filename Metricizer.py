import sys
import os

# sys.path.append('../')

import GraphQL.py
import REST.py
# From .env import load_.env load_dotenv()

print(sys.argv)

if len(sys.argv) != 2:
    print("ERROR. Proper use: python3 Metricizer/Metricizer url-file.txt")
    exit(1)
# for line in sys.stdin:
#     print(line)

# api_token = os.environ.get("GITHUB_TOKEN") 

# file_ptr = open(sys.argv[1])
# urls = file_ptr.readlines()

# for url in urls:
#     gql_info = call_graphQL(url, api_token)
#     rest_info = call_rest(url, api_token)

#     rampup = calc_rampup(info)
#     correctness = calc_correctness(info)
#     busfactor = calc_busfactor(info)
#     responsive_maintainer = calc_responsive_maintainer(info)
#     repo_license = calc_license(info)

def metricizer(inputfile):

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

        #Calculate metrics
        info = "deleteME"
        rampup = calc_rampup(info)
        correctness = calc_correctness(info)
        busfactor = calc_busfactor(info)
        responsive_maintainer = calc_responsive_maintainer(info)
        repo_license = calc_license(info)

        #Write metrics to metric output
        output_metric.write("Insert data here and a \n to finish it off.")

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
