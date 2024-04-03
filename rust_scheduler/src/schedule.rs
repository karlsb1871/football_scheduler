use crate::fixture::Fixture;



#[derive(Clone)]
pub struct Schedule {
    fixtures: Vec<Fixture>
}

impl Schedule {
    pub fn new(fixtures: Vec<Fixture>) -> Self {
        Self { fixtures }
    }
}