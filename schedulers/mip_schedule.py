import numpy as np
from schedulers.scheduler import Scheduler
from match import Match
from schedule import Schedule
from input_data import InputData
from scipy.optimize import milp, Bounds, LinearConstraint
import ast


class MIPScheduler(Scheduler):
    """
    This is an Abstract Base Class (ABC): it simply defines the base constructor and some public methods for
    all its children classes.
    You do not need to change anything in this class.
    """

    def __init__(self, *kwargs):
        super().__init__(*kwargs)

    def schedule(self) -> Schedule:
        var_names = self.variables()

        bounds = self.bounds()

        objective = self.objective()

        A, b_l, b_u = self.constraints()

        res = milp(
            c=objective,
            constraints=LinearConstraint(A, b_l, b_u),
            bounds=bounds,
            integrality=np.ones_like(objective),
            options={"disp": True},
        )

        print(res)
        non_zero = [var_name for var_name, xx in zip(var_names, res.x) if xx >= 0.5]

        matches = []
        for xx in non_zero:
            data = xx.split("_")
            home_idx = int(data[1])
            away_idx = int(data[2])
            date_idx = int(data[3])

            matches.append(
                Match(
                    home=self.teams[home_idx],
                    away=self.teams[away_idx],
                    date=self.dates[date_idx],
                    midweek=self.midweek[date_idx],
                )
            )

        return Schedule(matches)

    def variables(self):
        variables = []

        # X
        variables.extend(
            [
                f"x_{i}_{j}_{k}"
                for i in range(self.n_teams)
                for j in range(self.n_teams)
                for k in range(self.n_dates)
            ]
        )

        return variables

    def bounds(self):
        lower = []
        upper = []

        # X bounds
        lower.extend(
            [
                0
                for _ in range(self.n_teams)
                for _ in range(self.n_teams)
                for _ in range(self.n_dates)
            ]
        )
        upper.extend(
            [
                1
                for _ in range(self.n_teams)
                for _ in range(self.n_teams)
                for _ in range(self.n_dates)
            ]
        )

        return Bounds(lower, upper)

    def objective(self):
        # return self.distance_objective()
        return self.cancellation_probability_objective()
    
    def distance_objective(self):
        midweek_bool = self._input_data.midweek.values
        return np.array(
            [
                self._input_data.get_distance(home, away) if midweek else 0
                for home in self.teams
                for away in self.teams
                for midweek in midweek_bool
            ]
        )
    
    def cancellation_probability_objective(self):
        return np.array(
            [
                self._input_data.get_probability_of_cancellation(date, home)
                for home in self.teams
                for _ in self.teams
                for date in self.dates
            ]
        )



    def constraints(self):
        A = []
        b_l = []
        b_u = []

        # Every team must play everyone else at home
        # Which in turn satisfies that everyone must play everyone away
        for home in self.teams:
            for away in self.teams:
                if home != away:
                    A.append(
                        [
                            1 if home == hh and away == aa else 0
                            for hh in self.teams
                            for aa in self.teams
                            for mm in range(self.n_dates)
                        ]
                    )
                    b_l.extend([1])
                    b_u.extend([1])
                else:
                    A.append(
                        [
                            1 if home == hh and away == aa else 0
                            for hh in self.teams
                            for aa in self.teams
                            for mm in range(self.n_dates)
                        ]
                    )
                    b_l.extend([0])
                    b_u.extend([0])

        # Max one game per date
        for i in range(self.n_dates):
            for team in self.teams:
                A.append(
                    [
                        1 if (team == hh or team == aa) and i == mm else 0
                        for hh in self.teams
                        for aa in self.teams
                        for mm in range(self.n_dates)
                    ]
                )
                b_l.extend([0])
                b_u.extend([1])

        # Max number of home games in a row
        for i in range(self.n_dates - self.max_consecuative_home_games):
            for team in self.teams:
                A.append(
                    [
                        (
                            1
                            if team == hh
                            and mm
                            in [i + j for j in range(self.max_consecuative_home_games)]
                            else 0
                        )
                        for hh in self.teams
                        for _ in self.teams
                        for mm in range(self.n_dates)
                    ]
                )
                b_l.extend([0])
                b_u.extend([self.max_consecuative_home_games])

        # Teams that cannot both play at home same day
        for i in range(self.n_dates):
            pairs = [("Everton", "Liverpool")]
            for pair in pairs:
                A.append(
                    [
                        1 if (pair[0] == hh or pair[1] == hh) and i == mm else 0
                        for hh in self.teams
                        for aa in self.teams
                        for mm in range(self.n_dates)
                    ]
                )

                b_l.extend([0])
                b_u.extend([1])

        # Teams cannot play when unavailable
        for i in range(self.n_dates):
            if len(self.unavailable.iloc[i]) <= 2:
                continue
            unavailable = ast.literal_eval(self.unavailable.iloc[i])
            for team in self.teams:
                if team in unavailable:
                    A.append(
                        [
                            1 if (team == hh or team == aa) and i == mm else 0
                            for hh in self.teams
                            for aa in self.teams
                            for mm in range(self.n_dates)
                        ]
                    )

                    b_l.extend([0])
                    b_u.extend([0])

        return np.array(A), np.array(b_l), np.array(b_u)
