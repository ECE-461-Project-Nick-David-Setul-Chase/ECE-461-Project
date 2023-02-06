use std::fs::File;
use std::io::{ self, BufRead, BufWriter, Write};

pub const MIN_POSITIVE: f64 = 2.2250738585072014E-308f64;

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

    let mut scores: [f64; 6] = [0.0,0.0,0.0,0.0,0.0,0.0];

    // RampUp
    scores[0] =   num_comments / (num_lines - num_comments) * 0.5
                + readme_exists * 0.2
                + documentation_exists * 0.3;

    if scores[0] > 1.0 {
        scores[0] = 1.0;
    }
    if scores[0] < 0.0 {
        scores[0] = 0.0;
    }


    // Correctness
    scores[1] = 1.0 - (num_linter_warnings / (num_lines + MIN_POSITIVE)); // avoid divide by 0

    if scores[1] < 0.0 {
        scores[1] = 0.0;
    }

    // BusFactor
    scores[2] = 1.0 - (1.0 / (num_contributors + MIN_POSITIVE));

    if scores[2] < 0.0 {
        scores[2] = 0.0;
    }

    // ResponsiveMaintainer
    scores[3] = 1.0 / (num_issues + MIN_POSITIVE);
    
    if scores[3] > 1.0 {
        scores[3] = 1.0;
    }

    // CorrectLicense
    scores[4] = correct_license;

    // Total
    scores[5] =    scores[0] * 0.15
                + scores[1] * 0.2
                + scores[2] * 0.2
                + scores[3] * 0.15
                + scores[4] * 0.3;


    return scores;
}


fn main() {
    let line_reader = read_lines("test_score_data.txt".to_string());
    
    let metrics: Vec<f64> = line_reader
        .lines()
        .map(|x| x.unwrap().parse::<f64>().unwrap())
        .collect();

    println!("{:?}", metrics);

    let scores: [f64; 6] = calculate_scores(metrics);

    println!("{:?}", scores);

    let output_file = File::create("Scores.txt").unwrap();
    let mut writer = BufWriter::new(output_file);

    for score in scores {
        writeln!(writer, "{}", score);
    }

}