<a href="https://discord.gg/kKguSec" target="_blank">
    <img src="https://discord.com/api/guilds/565819215731228672/embed.png" alt="Support Discord server invite">
</a>
<a href="https://pypi.org/project/pss-fleet-data-client" target="_blank">
    <img src="https://img.shields.io/pypi/status/pss-fleet-data-client?color=%23DAB420&label=status" alt="Development status">
</a>
<a href="https://pypi.org/project/pss-fleet-data-client" target="_blank">
    <img src="https://img.shields.io/pypi/v/pss-fleet-data-client?color=%23DAB420&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/pss-fleet-data-client" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/pss-fleet-data-client.svg?color=%23DAB420" alt="Supported Python versions">
</a>

---

# Pixel Starships Fleet Data API client
An async client library for the [PSS Fleet Data API](https://github.com/Zukunftsmusik/pss-fleet-data-api).

# Features
- **Fully typehinted** so your favorite IDE can assist you with code completion.
- **Easy access** to any instance of a **PSS Fleet Data API** server.
- **Fast setup** to get you started quickly.

# Installation
**Python 3.11 or higher is required**

To install the library, run the following command:
```sh
pip install -U pss-fleet-data-client
```

# Code sample
To retrieve the last month's tournament results (a specific `Collection`):
```python
import asyncio
from datetime import datetime, timezone

from pss_fleet_data import ParameterInterval, PssFleetDataClient, utils

client = PssFleetDataClient(base_url="https://fleetdata.dolores2.xyz")

async def print_latest_tournament_results():
    now = datetime.now(tz=timezone.utc)
    most_recent_timestamp = utils.get_most_recent_timestamp(now, ParameterInterval.MONTHLY)
    collection = await client.get_most_recent_collection_by_timestamp(most_recent_timestamp)
    print(f"Collection with ID {collection.metadata.collection_id} collected at {collection.metadata.timestamp}.")
    print(f"It has collected {collection.metadata.fleet_count} fleets and {len(collection.users)} players.")

if __name__ == "__main__":
    asyncio.run(print_latest_tournament_results())
```
The library converts localized `datetime` objects to UTC or assumes UTC, if now `timezone` information is given. Any `datetime` objects returned are in UTC.

# Support
If you need help using the library or want to contribute, join my support Discord at: [discord.gg/kKguSec](https://https://discord.gg/kKguSec)

# Links
- Documentation (tbd)
- [Official Support Discord server](https://https://discord.gg/kKguSec)
- [PSS Fleet Data API](https://fleetdata.dolores2.xyz)
