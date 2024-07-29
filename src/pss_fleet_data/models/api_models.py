from datetime import datetime
from typing import Annotated, Any, Optional, Union

from pydantic import BaseModel, Field, field_validator

from ..core import utils
from ..core.config import CONFIG
from ..core.enums import UserAllianceMembershipEncoded


DATETIME = Annotated[datetime, Field(ge=CONFIG.pss_start_date)]
FLOAT_GE_0 = Annotated[float, Field(ge=0.0)]
INT_GE_0 = Annotated[int, Field(ge=0)]
INT_GE_1 = Annotated[int, Field(ge=1)]
STR_LENGTH_GE_1 = Annotated[str, Field(min_length=1)]

OPTIONAL_INT_GE_0 = Annotated[Optional[int], Field(ge=0, default=None)]
OPTIONAL_STR_LENGTH_GE_1 = Annotated[Optional[str], Field(min_length=1, default=None)]


ApiAlliance = tuple[
    INT_GE_1,
    STR_LENGTH_GE_1,
    INT_GE_0,
    INT_GE_0,
    OPTIONAL_INT_GE_0,
    OPTIONAL_INT_GE_0,
    OPTIONAL_INT_GE_0,
    OPTIONAL_INT_GE_0,
]
"""(
    0: alliance_id,
    1: alliance_name,
    2: score,
    3: division_design_id,
    4: trophy,
    5: championship_score,
    6: number_of_members,
    7: number_of_approved_members
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-7
"""


class ApiAllianceHistory(BaseModel):
    """
    A point in the recorded history of an Alliance.
    """

    collection: "ApiCollectionMetadata"
    """The metadata of the Collection that represents the point in the history of the Alliance."""
    fleet: ApiAlliance
    """The recorded Alliance data."""
    users: list["ApiUser"]
    """The members of the Alliance at the time of recording the Alliance data."""


class ApiCollection(BaseModel):
    """
    A snapshot of fleet and player data in PSS of the latest schema version.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions
    """

    metadata: "ApiCollectionMetadata"
    """The metadata of this Collection."""
    fleets: list[ApiAlliance] = Field(default_factory=lambda: list())
    """The fleets recorded in this Collection."""
    users: list["ApiUser"] = Field(default_factory=lambda: list())
    """The players recorded in this Collection."""


class ApiCollectionMetadata(BaseModel):
    """
    The metadata for a Collection of the latest schema version.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-9
    """

    timestamp: DATETIME
    """The timestamp of the moment the data in this Collection was started to get recorded."""
    duration: FLOAT_GE_0
    """The time it took to record the data in this Collection. In seconds."""
    fleet_count: INT_GE_0
    """The number of fleets recorded in this Collection."""
    user_count: INT_GE_0
    """The number of players recorded in this Collection."""
    tourney_running: bool
    """Determines, whether a monthly fleet tournament was running at the time of recording the data in this Collection."""
    data_version: Optional[int]
    """The schema version with which this data was first collected and stored."""
    collection_id: Optional[int]
    """The ID of the collection in the database."""
    schema_version: int
    """The version of the schema of the data in this Collection."""
    max_tournament_battle_attempts: Optional[int]
    """The maximum number of tournament battles any given player can do on a given monthly fleet tournament day."""

    @field_validator("timestamp", mode="before")
    @staticmethod
    def transform_timestamp(value: Any) -> Union[datetime, Any]:
        """Takes the value provided to set the property `timestamp`, parses it, localizes it to UTC and then removes the timezone information.

        Args:
            value (Any): The value to set. Will be transformed, if it's of type `datetime`, `int` or `str`.

        Raises:
            ValueError: Raised, if the parsed datetime is lower than the PSS start date.

        Returns:
            Union[datetime, Any]: The transformed datetime or the original value, if it's not been transformed.
        """
        if isinstance(value, (datetime, int, str)):
            result = utils.localize_to_utc(utils.parse_datetime(value))
            if result < CONFIG.pss_start_date:
                raise ValueError
            return result
        else:
            return value


class ApiErrorResponse(BaseModel):
    code: str
    message: str
    details: str
    timestamp: str
    url: str
    suggestion: str
    links: list["ApiLink"]


class ApiLink(BaseModel):
    """
    A simple dataclass to denote a hyperlink with a description in an API response.
    """

    path: str
    description: str

    def __str__(self) -> str:
        return self.__repr__

    def __repr__(self) -> str:
        return f"{self.path} ({self.description})"


ApiUser = tuple[
    INT_GE_1,
    STR_LENGTH_GE_1,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    UserAllianceMembershipEncoded,
    OPTIONAL_INT_GE_0,
    INT_GE_0,
    OPTIONAL_INT_GE_0,
    OPTIONAL_INT_GE_0,
    OPTIONAL_INT_GE_0,
    OPTIONAL_INT_GE_0,
    OPTIONAL_INT_GE_0,
    OPTIONAL_INT_GE_0,
    OPTIONAL_INT_GE_0,
    OPTIONAL_INT_GE_0,
    OPTIONAL_INT_GE_0,
    OPTIONAL_INT_GE_0,
    OPTIONAL_INT_GE_0,
    OPTIONAL_INT_GE_0,
]
"""(
    0: user_id,
    1: user_name,
    2: alliance_id,
    3: trophy,
    4: alliance_score,
    5: alliance_membership,
    6: alliance_join_date,
    7: last_login_date,
    8: last_heartbeat_date,
    9: crew_donated,
    10: crew_received,
    11: pvp_attack_wins,
    12: pvp_attack_losses,
    13: pvp_attack_draws,
    14: pvp_defence_wins,
    15: pvp_defence_losses,
    16: pvp_defence_draws,
    17: championship_score,
    18: highest_trophy,
    19: tournament_bonus_score
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-9
"""


class ApiUserHistory(BaseModel):
    """
    A point in the recorded history of a User.
    """

    collection: ApiCollectionMetadata
    """The metadata of the Collection that represents the point in the history of the Alliance."""
    user: ApiUser
    """The recorded User data."""
    fleet: Optional[ApiAlliance]
    """The Alliance of the User at the time of recording the User data. May be `None`, if the User was not in an Alliance at the time."""


__all__ = [
    "ApiAlliance",
    ApiAllianceHistory.__name__,
    ApiCollection.__name__,
    ApiCollectionMetadata.__name__,
    ApiErrorResponse.__name__,
    ApiLink.__name__,
    "ApiUser",
    ApiUserHistory.__name__,
]
