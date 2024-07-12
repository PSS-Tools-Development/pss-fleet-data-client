from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class Config:
    default_base_url: str = "https://fleetdata.dolores2.xyz"
    pss_start_date: datetime = datetime(2016, 1, 6, tzinfo=timezone.utc)


CONFIG = Config()
