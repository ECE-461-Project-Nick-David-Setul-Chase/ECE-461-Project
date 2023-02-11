use std::fs::File;
use std::io::{ self, BufRead, BufReader, Write};

pub const MIN_POSITIVE: f64 = 2.2250738585072014E-308f64;

fn main() {

    let lines = read_lines("test_score_data.txt".to_string());
    let mut full_metrics = Vec::new();

    for line in lines {
        let repo_metrics: Vec<String> = line.expect("failed to parse").split(",").map(str::to_string).collect();
        full_metrics.push(repo_metrics);
    }

    let full_scores = calculate_scores(full_metrics.clone());

    // write to output
    let scores_output_file = File::create("Scores.txt");
    for repo in 0..(full_scores.len() - 1) {
        for score in 0..6 {
            scores_output_file.as_ref().expect("failed to write").write(&full_scores[repo][score].as_bytes()).ok();
            scores_output_file.as_ref().expect("failed to write").write(", ".as_bytes()).ok();
        }
        scores_output_file.as_ref().expect("failed to write").write(&full_scores[repo][6].as_bytes()).ok();
        scores_output_file.as_ref().expect("failed to write").write("\n".as_bytes()).ok();
    }
    for score in 0..6 {
        scores_output_file.as_ref().expect("failed to write").write(&full_scores[full_scores.len()-1][score].as_bytes()).ok();
        scores_output_file.as_ref().expect("failed to write").write(", ".as_bytes()).ok();
    }
    scores_output_file.as_ref().expect("failed to write").write(&full_scores[full_scores.len()-1][6].as_bytes()).ok();

}

fn read_lines(filename: String) -> io::Lines<BufReader<File>> {
    let file = File::open(filename).unwrap(); 
    return io::BufReader::new(file).lines(); 
}

fn calculate_scores(full_metrics_strings: Vec<Vec<String>>) -> Vec<[String; 7]> {

    // for repo_metrics in full_metrics_strings:
        // define each variable

    let mut full_scores = Vec::new();

    for repo_metrics in full_metrics_strings {

        let repo_url: &str = &repo_metrics[0];
        let readme_exists: f64 = repo_metrics[1].parse().unwrap();
        let documentation_exists: f64 = repo_metrics[2].parse().unwrap();
        let issues_closed: f64 = repo_metrics[3].parse().unwrap();
        let issues_total: f64 = repo_metrics[4].parse().unwrap();
        let num_contributors: f64 = repo_metrics[5].parse().unwrap();
        let weeks_since_last_issue: f64 = repo_metrics[6].parse().unwrap();
        let license_correct: f64 = repo_metrics[7].parse().unwrap();

        let mut ramp_up: f64 = 0.5 * readme_exists + 0.5 * documentation_exists;
        let mut correctness: f64 = issues_closed / (issues_total + MIN_POSITIVE); // prevent divide by 0
        let mut bus_factor: f64 = 1.0 - (1.0 / num_contributors);
        let mut responsive_maintainer: f64 = 1.0 / (weeks_since_last_issue + MIN_POSITIVE); // prevent divide by 0
        let mut license: f64 = license_correct;

        if readme_exists == -1.0 { // url error 1
            ramp_up = -1.0;
            correctness = -1.0;
            bus_factor = -1.0;
            responsive_maintainer = -1.0;
            license = -1.0;
        }

        if readme_exists == -2.0 { // url error 2
            ramp_up = -2.0;
            correctness = -2.0;
            bus_factor = -2.0;
            responsive_maintainer = -2.0;
            license = -2.0;
        }

        let total: f64 = 0.15 * ramp_up + 
                         0.2 * correctness +
                         0.2 * bus_factor +
                         0.15 * responsive_maintainer +
                         0.3 * license;

        let repo_scores: [String; 7] = [repo_url.to_string(), 
                                        ramp_up.to_string(), 
                                        correctness.to_string(), 
                                        bus_factor.to_string(),
                                        responsive_maintainer.to_string(),
                                        license.to_string(),
                                        total.to_string()];

        full_scores.push(repo_scores);
    }

    return full_scores;

}