from KPIs.kpi import KPI
from schedule import Schedule


class UnplayedMatches(KPI):
    name = "Unplayed Matches"

    def __init__(self, *kwargs) -> None:
        super().__init__(*kwargs)

    def compute(self, schedule: Schedule):
        unplayed_matches = [
            match for match in schedule.matches if isinstance(match.date, float)
        ]

        return len(unplayed_matches)
