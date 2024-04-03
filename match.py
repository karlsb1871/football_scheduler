from dataclasses import dataclass
import datetime


@dataclass
class Match:
    home: str
    away: str
    date: datetime
    midweek: bool
