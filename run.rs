
// https://doc.rust-lang.org/book/ch01-02-hello-world.html
// https://doc.rust-lang.org/std/process/struct.Command.html
// https://doc.rust-lang.org/book/ch12-02-reading-a-file.html
// https://doc.rust-lang.org/rust-by-example/std/str.html
// https://doc.rust-lang.org/std/string/struct.String.html
// https://doc.rust-lang.org/rust-by-example/std/option.html
// https://doc.rust-lang.org/book/ch12-01-accepting-command-line-arguments.html
// https://doc.rust-lang.org/std/process/fn.exit.html
// https://doc.rust-lang.org/std/vec/struct.Vec.html

use std::process::Command;
use std::env;
use std::fs;
use std::process::exit;

fn main() {

    let args: Vec<String> = env::args().collect();
   
    if args.len() != 2 {
        // println!("use is ./run _____");
        exit(1);
    }

    let choice = &args[1];
    let mut status;

    if choice == "install" {
        status = execute_file("install.cmdln");
    } else if choice == "build" {
        status = execute_file("build.cmdln");
    } else if choice == "test" {
        status = execute_file("test.cmdln");
    } else {
        if choice != "URL_FILE" {
            let mut string = String::new();
            string.push_str("cp ");
            string.push_str(&choice);
            string.push_str(" URL_FILE");
            status = execute_string(string);
            if status != 0 {
                exit(status);
            }
        }
        status = execute_file("URL_FILE.cmdln");
    }

    if status != 0 {
        // println!("there was an error in execution"); 
    }

    exit(status);
}

fn execute_file(input_file: &str) -> i32 {

    let contents = fs::read_to_string(input_file)
        .expect("Should have been able to read file");

    let mut status_sum = 0;

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
                status_sum += execute_string(string);
            }

            string = String::new();
            is_comment = false;
            has_chars = false;
        } else {
            string.push(c);
        }
        //println!("{}", string);
    }

    return status_sum;
}

fn execute_string(string: String) -> i32 {
    // println!("About to run: {}", string);
    
    let mut iter = string.split_whitespace();

    let mut command = Command::new(iter.next().unwrap());
    
    let mut opt = iter.next();
    
    while opt != None {
        let arg = opt.unwrap();
        //println!("{}", arg);
        command.arg(arg);
        opt = iter.next();
    }

    let mut expect_str = String::new(); 
    let broke = " broke";
    expect_str.push_str(&string);
    expect_str.push_str(&broke);
    //println!("{}", expect_str);

    let status = command.status()
            .expect(&expect_str);
    
    if status.success() {
        return 0;
    } else {
        return 1;
    }
}
