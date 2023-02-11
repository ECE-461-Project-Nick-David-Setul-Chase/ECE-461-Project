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

    for repo_scores in full_scores {

        let repo_url: &str = &repo_scores[0];
        let ramp_up: f64 = repo_scores[1].parse().unwrap();
        let correctness: f64 = repo_scores[2].parse().unwrap();
        let bus_factor: f64 = repo_scores[3].parse().unwrap();
        let responsive_maintainer: f64 = repo_scores[4].parse().unwrap();
        let license: f64 = repo_scores[5].parse().unwrap();
        let total: f64 = repo_scores[6].parse().unwrap();

        if ramp_up == -1.0 { // url error 1
            println!("Repository URL: {}", repo_url);
            println!("    URL not supported - error 1");
        }
        if ramp_up == -2.0 { // url error 1
            println!("Repository URL: {}", repo_url);
            println!("    URL not supported - error 2");
        }
        if ramp_up == -3.0 { // api error
            println!("API error - could not access repositories.");
            exit(1);
        }
        else {
            println!("Repository URL: {}", repo_url);
            println!("    NetScore: {}", total);
            println!("        RampUp: {}", ramp_up);
            println!("        Correctness: {}", correctness);
            println!("        BusFactor: {}", bus_factor);
            println!("        ResponsiveMaintainer: {}", responsive_maintainer);
            println!("        License: {}", license);
        }
    }

}

fn read_lines(filename: String) -> io::Lines<BufReader<File>> {
    let file = File::open(filename).unwrap(); 
    return io::BufReader::new(file).lines(); 
}