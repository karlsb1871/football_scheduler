import pandas as pd


class InputData:
    def __init__(
        self, distances: pd.DataFrame, dates: pd.DataFrame, probabilities: pd.DataFrame
    ) -> None:
        self._distances = distances
        self._dates = dates
        self._probabilities = probabilities
        self._n_teams = len(distances.index)
        self._n_dates = len(dates.index)
        self._teams = distances.index

    @classmethod
    def from_csv(cls, folder_path: str):
        distances = pd.read_csv(f"{folder_path}/distances.csv", index_col=0)
        distances.fillna(0, inplace=True)

        # Define a custom converter function to convert string representation of lists to actual lists
        def convert_to_list(string):
            if string.startswith("[") and string.endswith("]"):
                return eval(
                    string
                )  # Evaluate the string as a Python expression to get the list
            else:
                return []

        # Define the converters dictionary with the custom converter for the "Unavailable_Teams" column
        converters = {"Unavailable_Teams": convert_to_list}

        dates = pd.read_csv(
            f"{folder_path}/dates.csv", index_col=0, converters=converters
        )

        # Get probabilities
        probabilities = pd.read_csv(f"{folder_path}/probabilities.csv", index_col=0)

        return InputData(distances, dates, probabilities)

    def get_distance(self, home, away):
        return self._distances[home][away]

    def get_probability_of_cancellation(self, date, home):
        return self._probabilities.loc[date][home]

    @property
    def n_teams(self):
        return self._n_teams

    @property
    def teams(self):
        return self._teams

    @property
    def n_dates(self):
        return self._n_dates

    @property
    def dates(self):
        return self._dates.index

    @property
    def midweek(self):
        return self._dates["Midweek"]

    @property
    def unavailabile(self):
        return self._dates["Unavailable"]
