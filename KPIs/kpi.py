from abc import abstractmethod

from input_data import InputData
from schedule import Schedule


class KPI:
    name = None

    def __init__(self, input_data: InputData) -> None:
        self.input_data = input_data

    @abstractmethod
    def compute(self, schedule: Schedule):
        pass
