extern crate csv;

use serde::{Deserialize};
use std::error::Error;
use std::fs::File; // Import the Deserialize trait
use chrono::{NaiveDate};

#[derive(Debug, Deserialize)]
pub struct Dates {
    #[serde(deserialize_with = "date_from_string")]
    pub Date: NaiveDate,
    pub Week: i32,
    #[serde(deserialize_with = "bool_from_string")]
    pub Midweek: bool,
    #[serde(deserialize_with = "vec_string_from_string")]
    pub Unavailable: Vec<String>,
}

// Custom deserialization function for date values
fn date_from_string<'de, D>(deserializer: D) -> Result<NaiveDate, D::Error>
where
    D: serde::Deserializer<'de>,
{
    let date_string: String = Deserialize::deserialize(deserializer)?;
    let date = NaiveDate::parse_from_str(&date_string, "%Y-%m-%d");
    match date {
        Ok(d) => Ok(d),
        _ => Err(serde::de::Error::custom("Error with date"))
    }
}

// Custom deserialization function for bool values
fn bool_from_string<'de, D>(deserializer: D) -> Result<bool, D::Error>
where
    D: serde::Deserializer<'de>,
{
    let s: String = Deserialize::deserialize(deserializer)?;
    match s.as_str() {
        "True" => Ok(true),
        "False" => Ok(false),
        _ => Err(serde::de::Error::custom("Invalid boolean value")),
    }
}

// Custom deserialization function for vec of strings
fn vec_string_from_string<'de, D>(deserializer: D) -> Result<Vec<String>, D::Error>
where
    D: serde::Deserializer<'de>,
{
    let input_string: String = Deserialize::deserialize(deserializer)?;
    // Remove the surrounding square brackets and split by ', '
    let inner_string = input_string.trim_start_matches('[').trim_end_matches(']');
    let parts: Vec<&str> = inner_string.split(", ").collect();

    // Convert each part to a string
    let mut strings: Vec<String> = Vec::new();
    for part in parts {
        // Remove the surrounding single quotes and push to the vector
        let cleaned_part = part.trim().trim_matches('\'');
        strings.push(cleaned_part.to_string());
    }

    Ok(strings)
}

pub fn read_dates() -> Result<Vec<Dates>, Box<dyn Error>> {
    // Path to your CSV file
    let csv_file_path = "../data/dates.csv";

    // Open the CSV file
    let file = File::open(csv_file_path)?;

    // Create a CSV reader
    let mut csv_reader = csv::ReaderBuilder::new()
        .has_headers(true)
        .from_reader(file);

    // Iterate over each record in the CSV file
    let mut dates : Vec<Dates> = vec![];
    for result in csv_reader.deserialize::<Dates>() {
        // Extract the record
        let record: Dates = result?;

        // Process the record (in this example, just print it)
        dates.push(record)
    }

    Ok(dates)
}
