use std::{error::Error, fs::File};
use array2d::Array2D;
use csv::ReaderBuilder;

pub fn read_distances() -> Result<(Array2D<f32>, Vec<String>), Box<dyn Error>> {
    // Path to your CSV file
    let csv_file_path = "../data/distances.csv";

    // Open the CSV file
    let file = File::open(csv_file_path)?;

    // Create a CSV reader
    let mut csv_reader = ReaderBuilder::new()
    .has_headers(true)
    .trim(csv::Trim::All)
    .from_reader(file);

    // Read the CSV headers to get row and column headers
    let headers = csv_reader.headers()?.clone();
    let headers: Vec<String> = headers.into_iter().skip(1).map(|s| s.to_string()).collect();
    println!("headers = {:?}", headers);
    // Count the number of rows and columns
    let num_rows = headers.len();
    let num_cols = num_rows; // Assuming it's a square matrix

    // Create an empty array to store the data
    let mut data = vec![vec![0.0f32; num_cols]; num_rows];

    // Read CSV records and populate the data array
    for (i, record) in csv_reader.records().enumerate() {
        let record = record?;
        for (j, value) in record.iter().skip(1).enumerate() {
            println!("value = {:?}", value);
            data[i][j] = match value {
                "" => 0.0,
                _ => value.parse::<f32>()?
            }
            // data[i][j] = 
        }
    }
    println!("data = {:?}", data[0]);

    let array = match Array2D::from_rows(&data) {
        Ok(a) => a,
        _ => panic!("Something went wrong with array!")
    };

    let result = (array, headers);

    Ok(result)
}