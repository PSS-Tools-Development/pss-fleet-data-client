from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class Config:
    """
    The base configuration of a PssFleetDataClient.
    """

    default_base_url: str = "https://fleetdata.dolores2.xyz"
    """The default base url of the Fleet Data API server."""
    pss_start_date: datetime = datetime(2016, 1, 6, tzinfo=timezone.utc)
    """The day Pixel Starships open beta started."""


__CONFIG = Config()


def get_config() -> Config:
    return __CONFIG
