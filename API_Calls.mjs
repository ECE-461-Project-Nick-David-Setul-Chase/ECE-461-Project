import { Octokit } from "octokit";

const octokit = new Octokit({
  // Access token goes here
});
  

const response = await octokit.request('GET /repos/{owner}/{repo}/collaborators{?affiliation,permission,per_page,page}', {
  owner: 'jonschlinkert',
  repo: 'even'
})
  
  console.log(`The status of the response is: ${response.status}`)
  console.log(`The request URL was: ${response.url}`)
  console.log(`The x-ratelimit-remaining response header is: ${response.headers["x-ratelimit-remaining"]}`)
  console.log(`The issue title is: ${response.data.title}`)
  