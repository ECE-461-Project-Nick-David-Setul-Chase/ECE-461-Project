
// https://doc.rust-lang.org/book/ch01-02-hello-world.html
// https://doc.rust-lang.org/std/process/struct.Command.html
// https://doc.rust-lang.org/book/ch12-02-reading-a-file.html
// https://doc.rust-lang.org/rust-by-example/std/str.html

//use std::process::Command;
//use std::env;
use std::fs;

fn main() {

    let input_file = "run_URL_FILE.txt";

    println!("In file {}", input_file);

    execute_file(input_file);
}

fn execute_file(input_file: &str) {

    let contents = fs::read_to_string(input_file)
        .expect("Should have been able to read file");

    let chars: Vec<char> = contents.chars().collect();
    let mut string = String::new();
    let mut is_comment = false;
    let mut has_chars = false;

    for c in chars {
        if c == '#' {
            is_comment = true;
        } else  if c != ' ' && c != '\n' && c != '\t' {
            has_chars = true;
        } 

        if c == '\n' {
            if !is_comment && has_chars {
                println!("{}", string);
            }

            string = String::new();
            is_comment = false;
            has_chars = false;
        } else {
            string.push(c);
        }
        //println!("{}", string);
    }

    //println!("With text:\n{contents}");

    /*Command::new("python3")
            .arg("Metricizer.py")
            .arg(input_file)
            //.arg("ScorerModule.rs")
            //.arg("Output.rs")
            .spawn()
            .expect("Metricizer failed to start");
*/
}
/*
fn execute_string(string) {
    
}*/
