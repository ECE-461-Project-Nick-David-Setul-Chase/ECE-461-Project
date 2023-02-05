import sys

# sys.path.append('../')

import GraphQL.py
# From .env import load_.env load_dotenv()


import os

print(sys.argv)

if len(sys.argv) != 2:
    print("ERROR. Proper use: python3 Metricizer/Metricizer url-file.txt")
    exit(1)
# for line in sys.stdin:
#     print(line)

api_token = os.environ.get("GITHUB_TOKEN") 

file_ptr = open(sys.argv[1])
urls = file_ptr.readlines()

for url in urls:
    gql_info = call_graphQL(url, api_token)
    rest_info = call_rest(url, api_token)

    rampup = calc_rampup(info)
    correctness = calc_correctness(info)
    busfactor = calc_busfactor(info)
    responsive_maintainer = calc_responsive_maintainer(info)
    repo_license = calc_license(info)


def rampup(info):
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
