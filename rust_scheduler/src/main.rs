use rust_scheduler::input_data::InputData;
use rust_scheduler::schedulers::scheduler::Scheduler;
use rust_scheduler::schedulers::simulated_annealing::SimulatedAnnealing;

fn main() {
    println!("Hello, world!");

    let input_data = InputData::new();

    let scheduler = SimulatedAnnealing::new(31.0, 0.99, 1000, 100);

    let final_schedule = scheduler.schedule();
}
