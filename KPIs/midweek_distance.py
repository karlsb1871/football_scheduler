from KPIs.kpi import KPI
from schedule import Schedule


class MidweekDistance(KPI):
    name = "Midweek Distance"

    def __init__(self, *kwargs) -> None:
        super().__init__(*kwargs)

    def compute(self, schedule: Schedule):
        midweek_matches = [match for match in schedule.matches if match.midweek]
        distances = [
            self.input_data.get_distance(match.home, match.away)
            for match in midweek_matches
        ]

        return sum(distances)
