use crate::{dates::{read_dates, Dates}, distances::read_distances};
use array2d::Array2D;
pub struct InputData {
    pub dates: Vec<Dates>,
    pub distances: Array2D<f32>
}

impl InputData {
    pub fn new() -> Self {
        let dates = read_dates();
        let dates = match dates {
            Ok(d) => d,
            _ => panic!("Something wrong with dates!")
        };

        let distances = read_distances();
        println!("distances = {:?}", distances);
        let distances = Array2D::filled_with(0.0, 20, 30);

        Self {
            dates,
            distances
        }
    }
}