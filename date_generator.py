import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from datetime import datetime, timedelta
from scipy.stats import poisson

# Fix seed
np.random.seed(0)

# Define start and end dates
start_date = datetime(2023, 8, 12)
end_date = datetime(2024, 5, 19)

# Define a timedelta of one day
one_day = timedelta(days=1)

# Initialize lists to store data
dates = []
week_numbers = []
is_tuesdays = []
unavailable = []
teams = [
    "Arsenal",
    "Aston Villa",
    "Bournemouth",
    "Brentford",
    "Brighton and Hove Albion",
    "Burnley",
    "Chelsea",
    "Crystal Palace",
    "Everton",
    "Fulham",
    "Liverpool",
    "Luton Town",
    "Manchester City",
    "Manchester United",
    "Newcastle United",
    "Nottingham Forest",
    "Sheffield United",
    "Tottenham Hotspur",
    "West Ham United",
    "Wolverhampton Wanderers",
]

cup_competitions = {
    "Champions League": {"dates": [], "teams": []},
    "FA Cup": {date: teams.copy() for date in [datetime(2024, 1, 6)]},
    "International": {
        date: teams.copy()
        for date in [
            datetime(2023, 9, 5),
            datetime(2023, 9, 9),
            datetime(2023, 9, 12),
            datetime(2023, 10, 10),
            datetime(2023, 10, 14),
            datetime(2023, 10, 17),
            datetime(2023, 11, 14),
            datetime(2023, 11, 18),
            datetime(2023, 11, 21),
            datetime(2024, 3, 19),
            datetime(2024, 3, 23),
            datetime(2024, 3, 26),
        ]
    },
}

# Loop through the dates
current_date = start_date
week_counter = 1
while current_date <= end_date:
    # Check if the current date is a Tuesday or Saturday
    if current_date.weekday() == 1 or current_date.weekday() == 5:
        # Append data to lists
        dates.append(current_date)
        week_numbers.append(week_counter)
        is_tuesdays.append(current_date.weekday() == 1)

        unavailable_teams = []
        # Loop through cup competitions
        for cup_name, cup_details in cup_competitions.items():
            for date, teams in cup_details.items():
                if current_date == date:
                    unavailable_teams.extend(teams)

        unavailable.append(unavailable_teams)

    # Move to the next day
    current_date += one_day

    # If it's Saturday, increment the week counter
    if current_date.weekday() == 5:
        week_counter += 1

# Create a DataFrame
df = pd.DataFrame(
    {
        "Date": dates,
        "Week": week_numbers,
        "Midweek": is_tuesdays,
        "Unavailable": unavailable,
    },
    index=dates,
)

# Save the DataFrame to a CSV file
df.to_csv("data/dates.csv", index=False)


# Function to generate dates for Tuesdays and Saturdays between two dates
def generate_dates(start_date, end_date):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == 1 or current_date.weekday() == 5:
            dates.append(current_date)
        current_date += timedelta(days=1)
    return dates


# Define start and end dates
# start_date = datetime(2023, 8, 1)
# end_date = datetime(2024, 5, 27)

# Generate dates for Tuesdays and Saturdays
dates = generate_dates(start_date, end_date)

df = pd.DataFrame(index=dates)

# Define the first week of December
december_start = datetime(2023, 12, 1)

# Calculate probabilities following Poisson distribution centered around the first week of December
for team in teams:
    # Define parameters
    size = len(dates)  # Length of the array
    peak_value = np.random.rand()  # Value at the peak (40th value)
    peak_index = int(size / 2)  # Index of the peak value

    print(f"{team} {peak_value}")

    # Generate increasing and decreasing sequences
    increasing_values = np.linspace(0, peak_value, peak_index)
    decreasing_values = np.linspace(peak_value, 0, size - peak_index)

    # Concatenate the sequences
    values = np.concatenate([increasing_values, decreasing_values])
    df[team] = values

# Write DataFrame to CSV
df.to_csv("premier_league_probabilities.csv")
