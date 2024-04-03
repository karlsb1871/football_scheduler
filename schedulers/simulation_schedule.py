import ast
from datetime import datetime
import math
import random
from KPIs.midweek_distance import MidweekDistance
from KPIs.unplayed_matches import UnplayedMatches
from match import Match
from schedule import Schedule
from schedulers.scheduler import Scheduler
import numpy as np
import copy


class SimulationSchedule(Scheduler):
    def __init__(self, *kwargs):
        super().__init__(*kwargs)
        self.kpis = [
            MidweekDistance(self._input_data),
            UnplayedMatches(self._input_data),
        ]

    def schedule(self) -> Schedule:
        # Generate initial schedule
        initial_schedule = Schedule([])
        initial_schedule.from_csv("output/mip_schedule.csv")
        initial_matches = initial_schedule.matches.copy()

        # Initial parameters
        temp = 31
        cooling_rate = 0.99
        n_iterations = 10000
        np.random.seed(0)

        # Evaluate initial schedule
        initial_results = self.evaluate(initial_schedule)

        # Update incumbent
        current_schedule = initial_schedule
        current_results = initial_results
        incumbent_schedule = initial_schedule
        incumbent_results = initial_results
        incumbent_schedule.to_csv("output/neighbour.csv")
        print(incumbent_results)

        # For loop
        for i in range(n_iterations):
            print("\n")
            neighbour = self.neighbour(current_schedule)
            neighbour_results = self.evaluate(neighbour)
            print(f"Current = {current_results}")
            print(f"Neighbour = {neighbour_results}")
            print(f"Incumbent = {incumbent_results}")

            delta_energy = (
                neighbour_results["Unplayed Matches"]
                - current_results["Unplayed Matches"]
            )

            if self.acceptance_probability(delta_energy, temp) > np.random.random():
                print("Neighbour Accepted")
                current_schedule = neighbour
                current_results = neighbour_results

            if (
                neighbour_results["Unplayed Matches"]
                < incumbent_results["Unplayed Matches"]
            ):
                print("Incumbent Updated")
                incumbent_schedule = neighbour
                incumbent_results = neighbour_results
                incumbent_schedule.to_csv("output/incumbent_schedule.csv")

            temp *= cooling_rate

        incumbent_schedule.to_csv("output/incumbent_schedule.csv")

        pass
        return incumbent_schedule

    # Define the acceptance probability function
    def acceptance_probability(self, delta, temperature):
        print(f"{delta=}")
        if delta < 0:
            return 1.0
        print(math.exp(-delta / temperature))
        return math.exp(-delta / temperature)

    def evaluate(self, schedule: Schedule):
        kpi_results = {kpi.name: [] for kpi in self.kpis}
        for _ in range(350):
            sim_schedule = copy.deepcopy(schedule)
            final_schedule = self.simulation(sim_schedule)
            for kpi in self.kpis:
                kpi_results[kpi.name].append(kpi.compute(final_schedule))

        stats_results = {key: np.average(value) for key, value in kpi_results.items()}
        std = {key: np.std(value) for key, value in kpi_results.items()}
        print(f"{std=}")
        return stats_results

    def simulation(self, schedule: Schedule):

        for date in self.dates:
            matches = [match for match in schedule.matches if match.date == date]
            probabilities = [
                self._input_data.get_probability_of_cancellation(match.date, match.home)
                for match in matches
            ]
            cancelled_matches = [
                match
                for match, probability in zip(matches, probabilities)
                if np.random.rand() <= probability
            ]

            if len(cancelled_matches) > 0:
                self.reschedule(schedule, cancelled_matches)
        return schedule

    def reschedule(self, schedule: Schedule, cancelled_matches: list[Match]):
        for match in cancelled_matches:
            for future_date in self.dates[self.dates > match.date]:
                future_date_index = list(self.dates).index(future_date)
                unavailable = ast.literal_eval(self.unavailable.iloc[future_date_index])
                future_matches = [
                    m
                    for m in schedule.matches
                    if m.date == future_date
                    # and (m.home in unavailable or m.away in unavailable)
                    and (
                        m.home in [match.home, match.away]
                        or m.away in [match.home, match.away]
                    )
                ]
                if future_date == "2023-09-05":
                    pass
                if (
                    len(future_matches) == 0
                    and match.home not in unavailable
                    and match.away not in unavailable
                ):
                    match.date = future_date
                    match.midweek = self.midweek[future_date_index]
                    break
                else:
                    continue
            else:
                match.date = np.nan

    def neighbour(self, schedule: Schedule):
        random_int = np.random.randint(0,2)
        if random_int == 0:
            print("Moving fixture")
            schedule = self.move_random_fixture(schedule)
        elif random_int == 1:
            print("Flipping fixture")
            schedule = self.flip_home_and_away_teams(schedule)

        return schedule
    
    def flip_home_and_away_teams(self, schedule: Schedule):
        # A neighbour is found by swapping the home/away versions of a fixture
        neighbour = copy.deepcopy(schedule)
        match = random.choices(
            neighbour.matches,
            weights=[
                self._input_data.get_probability_of_cancellation(m.date, m.home)
                for m in neighbour.matches
            ],
            k=1,
        )[0]

        reverse_match = [m for m in neighbour.matches if m.home == match.away and m.away == match.home][0]
        print(f"Match {match} to {reverse_match.date}")
        print(f"Match {reverse_match} to {match.date}")

        match.date, reverse_match.date = reverse_match.date, match.date
        match.midweek, reverse_match.midweek = reverse_match.midweek, match.midweek
        return neighbour

    def move_random_fixture(self, schedule: Schedule):
        # A neighbour is found by moving a random fixture to a free date
        neighbour = copy.deepcopy(schedule)
        # match_index = np.random.randint(low=0, high=len(neighbour.matches))
        # match = neighbour.matches[match_index]
        match = random.choices(
            neighbour.matches,
            weights=[
                self._input_data.get_probability_of_cancellation(m.date, m.home)
                for m in neighbour.matches
            ],
            k=1,
        )[0]

        while True:
            # rand_date_index = np.random.randint(low=0, high=len(self.dates))
            rand_date_index = random.choices(
                list(range(self.n_dates)),
                weights=[
                    1
                    - self._input_data.get_probability_of_cancellation(date, match.home)
                    for date in self.dates
                ],
            )[0]

            rand_date = self.dates[rand_date_index]
            if rand_date == match.date:
                continue

            unavailable = ast.literal_eval(self.unavailable.iloc[rand_date_index])
            if match.home in unavailable or match.away in unavailable:
                continue
            games = []
            for m in schedule.matches:
                if m.date == rand_date and (
                    m.home in [match.home, match.away]
                    or m.away in [match.home, match.away]
                ):
                    games.append(m)
                    break

            if len(games) > 0:
                continue
            else:
                print(f"Match {match} to {rand_date}")
                match.date = rand_date
                match.midweek = self.midweek[rand_date_index]
                break

        return neighbour
