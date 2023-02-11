import sys
import os
# From .env import load_.env load_dotenv()
from GraphQL import call_graphQL
from REST import call_rest
# sys.path.append('../')

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
        
        #if url is not githup or npm
            #error
        #else if it is npm
            #web scrap for github

        #if git hub .
            #yay
        
        #Grab list from APIs --- [readme_exist, doc_exist, issues_closed, issues_total, num_contribute, weeks_last_issue, license_correct]
        gql_info = call_graphQL(url, api_token)
        rest_info = call_rest(url, api_token)

        print(gql_info)
        print(rest_info)

        #Find metric params
        readme_exist = gql_info[0]
        doc_exist = gql_info[1]
        issues_closed = rest_info[2]
        issues_total = rest_info[3]
        num_contribute = gql_info[4]
        weeks_last_issue = gql_info[5]
        license_correct = gql_info[6]

        #Write metrics to metric output
        #Format: url,readme_exist,doc_exist,issues_closed,issues_total,num_contribute,weeks_last_issue,license_correct
        #Example: https://github.com/user/repo,1,1,45,64,5,2,1
        output_metric.write(url + "," + readme_exist + "," + doc_exist + "," + issues_closed + "," + issues_total + "," + num_contribute + "," + weeks_last_issue + "," + license_correct + "\n")

    #Closing all files
    file_ptr.close()
    output_metric.close()

#####################################################
if __name__ == '__main__':
    metricizer("testurls.txt")