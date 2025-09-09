use std::time::Instant;

fn calculate(iterations: u64, param1: f64, param2: f64) -> f64 {
    let mut result = 1.0;
    for i in 1..=iterations {
        let j1 = i as f64 * param1 - param2;
        result -= 1.0 / j1;
        let j2 = i as f64 * param1 + param2;
        result += 1.0 / j2;
    }
    result
}

fn main() {
    let start_time = Instant::now();
    let result = calculate(100_000_000, 4.0, 1.0) * 4.0;
    let end_time = Instant::now();

    println!("Result: {:.12}", result);
    println!("Execution Time: {:.6} seconds", (end_time - start_time).as_secs_f64());
}
