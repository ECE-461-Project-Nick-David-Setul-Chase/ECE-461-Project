use std::fs::File;
use std::io::{ self, BufRead};
use std::cmp;

fn read_lines(filename: String) -> io::BufReader<File> {
    let file = File::open(filename).unwrap(); 
    return io::BufReader::new(file); 
}

fn calculate_scores(metrics: Vec<f64>) -> [f64; 6] {

    let num_lines = metrics[0];
    let num_comments = metrics[1];
    let readme_exists = metrics[2];
    let documentation_exists = metrics[3];
    let num_linter_warnings = metrics[4];
    let num_contributors = metrics[5];
    let num_issues = metrics[6];
    let correct_license = metrics[7];

    let scores = [f64; 6];

    // RampUp
    scores[0] =   cmp::max(num_comments / (num_lines - num_comments), 1.0) * .5
                + readme_exists * .2
                + documentation_exists * .3;

    // Correctness
    scores[1] = 0;

    // BusFactor
    scores[2] = 0;

    // ResponsiveMaintainer
    scores[3] = 0;

    // CorrectLicense
    scores[4] = correct_license;

    // Total
    scores[5] =    scores[0] * .15
                + scores[1] * .2
                + scores[2] * .2
                + scores[3] * .15
                + scores[4] * .3;


    return scores;
}


fn main() {
    let line_reader = read_lines("test_score_data.txt".to_string());
    
    let metrics: Vec<f64> = line_reader
        .lines()
        .map(|x| x.unwrap().parse::<f64>().unwrap())
        .collect();

    println!("{:?}", metrics);
    
}