from datetime import datetime
from typing import Optional

from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser
from pydantic import BaseModel, ConfigDict


class AllianceHistory(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    collection: "CollectionMetadata"
    alliance: PssAlliance
    users: list[PssUser]


class Collection(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    metadata: "CollectionMetadata"
    alliances: list[PssAlliance]
    users: list[PssUser]


class CollectionMetadata(BaseModel):
    collection_id: Optional[int] = None
    """The ID of the collection in the database."""
    timestamp: datetime
    """The timestamp of the moment the data in this Collection was started to get recorded."""
    duration: float
    """The time it took to record the data in this Collection. In seconds."""
    fleet_count: int
    """The number of fleets recorded in this Collection."""
    user_count: int
    """The number of players recorded in this Collection."""
    tournament_running: bool
    """Determines, whether a monthly fleet tournament was running at the time of recording the data in this Collection."""
    schema_version: int
    """The version of the schema of the data in this Collection."""
    max_tournament_battle_attempts: Optional[int] = None
    """The maximum number of tournament battles any given player can do on a given monthly fleet tournament day."""
    data_version: Optional[int]
    """The schema version with which this data was first collected and stored."""


class UserHistory(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    collection: "CollectionMetadata"
    user: PssUser
    alliance: Optional[PssAlliance]
