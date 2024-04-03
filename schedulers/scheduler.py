from abc import abstractmethod
import numpy as np
from match import Match
from schedule import Schedule
from input_data import InputData
from scipy.optimize import milp, Bounds, LinearConstraint
import ast


class Scheduler:
    """
    This is an Abstract Base Class (ABC): it simply defines the base constructor and some public methods for
    all its children classes.
    You do not need to change anything in this class.
    """

    def __init__(self, input_data: InputData):
        self._input_data = input_data
        self.n_teams = input_data.n_teams
        self.teams = input_data.teams
        self.n_dates = input_data.n_dates
        self.dates = input_data.dates
        self.midweek = self._input_data.midweek.values
        self.max_consecuative_home_games = 3
        self.max_dates_without_game = 3
        self.unavailable = input_data.unavailabile

    @abstractmethod
    def schedule(self) -> Schedule:
        pass
