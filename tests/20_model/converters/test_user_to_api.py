from datetime import datetime

import pytest
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from src.client.model import AllianceHistory, Collection, CollectionMetadata, UserHistory
from src.client.model.api import ApiAlliance, ApiAllianceHistory, ApiCollection, ApiCollectionMetadata, ApiUser, ApiUserHistory
from src.client.model.converters import FromAPI


# Helpers
