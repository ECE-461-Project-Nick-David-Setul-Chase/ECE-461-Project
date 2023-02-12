use std::fs::File;
use std::process::exit;
use std::io::{ self, BufRead, BufReader};

fn main() {

    let lines = read_lines("Scores.txt".to_string());
    let mut full_scores = Vec::new();

    for line in lines {
        let repo_scores: Vec<String> = line.expect("failed to parse").split(",").map(str::to_string).collect();
        full_scores.push(repo_scores);
    }

    for i in 0..full_scores.len() {
        for j in 0..full_scores.len() - i - 1 {
            if full_scores[j + 1][6] > full_scores[j][6] {
                full_scores.swap(j, j + 1);
            }
        }
    }

    for repo_scores in full_scores {

        let repo_url: &str = &repo_scores[0];
        let ramp_up: f64 = repo_scores[1].parse().unwrap();
        let correctness: f64 = repo_scores[2].parse().unwrap();
        let bus_factor: f64 = repo_scores[3].parse().unwrap();
        let responsive_maintainer: f64 = repo_scores[4].parse().unwrap();
        let license: f64 = repo_scores[5].parse().unwrap();
        let total: f64 = repo_scores[6].parse().unwrap();

        if ramp_up == -1.0 { // url error 1
            println!("Repository URL: {} is not supported - no GitHub link found on NPM page", repo_url);
        }
        else if ramp_up == -2.0 { // url error 2
            println!("Repository URL: {} is not supported - url is not NPM or GitHub", repo_url);
        }
        else if ramp_up == -3.0 { // api error
            println!("API error - could not access repositories.");
            exit(1);
        }
        else {
            println!("{{\"URL\":\"{}\", \"NET_SCORE\":{}, \"RAMP_UP_SCORE\":{}, \"CORRECTNESS_SCORE\":{}, \"BUS_FACTOR_SCORE\":{}, \"RESPONSIVE_MAINTAINER_SCORE\":{}, \"LICENSE_SCORE\":{}}}", repo_url, total, ramp_up, correctness, bus_factor, responsive_maintainer, license);
        }
    }

}

fn read_lines(filename: String) -> io::Lines<BufReader<File>> {
    let file = File::open(filename).unwrap(); 
    return io::BufReader::new(file).lines(); 
}