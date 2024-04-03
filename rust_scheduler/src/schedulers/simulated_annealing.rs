use crate::{schedule::{self, Schedule}, schedulers::{kpi::KPI, scheduler::Scheduler}};

pub struct SimulatedAnnealing {
    initial_temperature: f32,
    cooling_rate: f32,
    n_iterations: i32,
    n_monte_carlo_simulations: i32
}

impl SimulatedAnnealing {
    pub fn new(initial_temperature: f32, cooling_rate: f32, n_iterations: i32, n_monte_carlo_simulations: i32) -> Self {
        Self {
            initial_temperature,
            cooling_rate,
            n_iterations,
            n_monte_carlo_simulations
        }
    }

    fn generate_neighbour(&self) -> Schedule {
        todo!()
    }

    fn evaluate(&self, schedule: Schedule) -> KPI {
        todo!()
    }
}

impl Scheduler for SimulatedAnnealing {
    fn schedule(self) -> Schedule {
        // Get initial schedule
        let current_schedule = Schedule::new(vec![]);
        let incumbent_schedule = current_schedule.clone();
        
        for i in 0..self.n_iterations {
            println!("Iteration = {:?}",i);
            // Generate neighbour
            let neighbour = self.generate_neighbour();
            let neighbour_results = self.evaluate(neighbour);

            // Determine delta


        }
        todo!()
    }
}
