
// https://doc.rust-lang.org/book/ch01-02-hello-world.html
// https://doc.rust-lang.org/std/process/struct.Command.html

fn main() {
    println!("Hello, world!");

    use std::process::Command;

    let input_file = "sample-url-file.txt";

    Command::new("python3")
            .arg("Metricizer/Metricizer.py")
            .arg(input_file)
            .spawn()
            .expect("Metricizer failed to start");


}