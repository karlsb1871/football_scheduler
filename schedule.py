import pandas as pd

from match import Match


class Schedule:
    def __init__(self, matches: list[Match]) -> None:
        self.matches = matches

    def to_csv(self, output_file: str):
        df = pd.DataFrame(
            {
                "Date": [match.date for match in self.matches],
                "Home": [match.home for match in self.matches],
                "Away": [match.away for match in self.matches],
                "Midweek": [match.midweek for match in self.matches],
            }
        )

        # Convert the "Date" column to datetime
        df["Date"] = pd.to_datetime(df["Date"])

        # Sort the DataFrame by "Date" and "Home"
        df = df.sort_values(by=["Date", "Home"])

        # Set index
        df.set_index("Date", inplace=True)

        df.to_csv(output_file)

    def from_csv(self, file_name):
        df = pd.read_csv(file_name)

        matches = []
        for i, row in df.iterrows():
            matches.append(Match(row["Home"], row["Away"], row["Date"], row["Midweek"]))

        self.matches = matches
