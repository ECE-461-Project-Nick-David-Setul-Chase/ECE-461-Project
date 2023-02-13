# ECE-461-Project - Repository URL Analyzer
Nicholas Williams, David Reed, Setul Parekh, Chase McCoy

# General Information

## Supported URLs 
  * GitHub
  * NPM (only with a corresponding GitHub URL)

## License Support
This software only recognizes [GNU GPL](https://www.gnu.org/licenses/license-list.en.html) supported free licenses.

# How to Use

## Download
To download this software, first clone the repository onto a Linux based platform.
Next, type and enter the command `./run install`
This will install all dependencies needed for proper software execution.

**Note:** In the unlikely event that the run executable file does not exist or work, 
          please type and enter `make` and then `./run install`

## Run
To run the software, a couple environment variables must be set. Otherwise, the code
will throw an error. Please create the environment variables listed below. To create 
these variables, simply type `export <ENV_VAR>=<VALUE>`.
  * `GITHUB_TOKEN` : Your personal GitHub token to access GitHub APIs
  * `LOG_LEVEL` : Either 0, 1, or 2. These determine the LOG file outputs.
  * `LOG_FILE` : The location you would like the LOG file to be created.

Once environment variables are set, type and enter `./run <URL_FILE>`, where URL_FILE is a text file containing the list of URLs you would like to analyze.
  
## Outputs
A LOG file output will be created in the location specified by the `LOG_FILE`
environment variable.

A list of URLs ranked from most trustworthy to least trustworthy, will be printed
to the CLI in ndjson format.

# System Architecture

## Brain
### run.rs
Description: Controls the data flow between modules.

## API
### GraphQL.py, REST.py
Description: Grabs data responses from both the GitHub GraphQL and REST APIs to be
used in metric calculations.

## Metricizer
### Metricizer.py
Description: Calls API methods to retrieve data to be processed for metric calculations.
Also sends data for each input URL to an output file for the scorer module to read.

## Scorer
### ScorerModule.rs
Description: Calculates metric scores and net scores for all URLs based on metricizer
data file output.

## Output
### OutputModule.rs
Description: Prints metric and net scores in ndjson format, ranked in order of highest
to lowest score.

# License & Rights
### Property of Purdue University ECE 461
### Developed and owned by Nicholas Williams, David Reed, Setul Parekh, Chase McCoy
Dependencies are supported by the [GNU GPL](https://www.gnu.org/licenses/license-list.en.html).
This software has no license support.


![Purdue CompE](https://media.licdn.com/dms/image/C560BAQFFhTOSK0IkUA/company-logo_200_200/0/1628271813820?e=2147483647&v=beta&t=t8XijiB1rlihGVKK4CmSVNxus8YNtV-pzuy91ssdSwE)
