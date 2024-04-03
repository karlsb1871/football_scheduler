use crate::schedule::Schedule;

pub trait Scheduler {
    fn schedule(self) -> Schedule;
}