# Pixel Starships Fleet Data API client

<a href="https://discord.gg/kKguSec" target="_blank"><img src="https://discord.com/api/guilds/565819215731228672/embed.png" alt="Support Discord server invite"></a>
<a href="https://pypi.org/project/pss-fleet-data-client" target="_blank"><img src="https://img.shields.io/pypi/status/pss-fleet-data-client?color=%23DAB420&label=status" alt="Development status"></a>
<a href="https://pypi.org/project/pss-fleet-data-client" target="_blank"><img src="https://img.shields.io/pypi/v/pss-fleet-data-client?color=%23DAB420&label=pypi%20package" alt="Package version"></a>
<a href="https://pypi.org/project/pss-fleet-data-client" target="_blank"><img src="https://img.shields.io/pypi/pyversions/pss-fleet-data-client.svg?color=%23DAB420" alt="Supported Python versions"></a>
<img src="https://img.shields.io/codecov/c/github/pss-tools-development/pss-fleet-data-client" alt="Code coverage">

> An async client library to access the [PSS Fleet Data API](https://github.com/Zukunftsmusik/pss-fleet-data-api). Currently supported API version is **1.5.0**.

## Built with

- [httpx](https://www.python-httpx.org/)
- [pssapi.py](https://pypi.org/project/pssapi)
- [pydantic V2](https://docs.pydantic.dev/latest/)

# ✨ Features

- **Fully typehinted** so your favorite IDE can assist you with code completion.
- **Easy access** to any instance of a **PSS Fleet Data API** server.
- **Fast setup** to get you started quickly.

# 🔍 Future plans

- Support more Python versions

# 🚀 Demo
To retrieve the last month's tournament results (a specific Collection):
```python
import asyncio
from datetime import datetime, timezone

from pss_fleet_data import ParameterInterval, PssFleetDataClient, utils

# Create the client, specifying the API server's base URL. If you don't specify a base URL, it defaults to https://fleetdata.dolores2.xyz
client = PssFleetDataClient(base_url="https://fleetdata.dolores2.xyz")

async def print_latest_tournament_results():
    # Get the current time
    now = datetime.now(tz=timezone.utc)

    # Tournament results are collected shortly before the start of a new month.
    # Calculate the most recent start of month relative to now.
    most_recent_timestamp = utils.get_most_recent_timestamp(now, ParameterInterval.MONTHLY)

    # Then get the most recent data collected before the calculated timestamp.
    collection = await client.get_most_recent_collection_by_timestamp(most_recent_timestamp)

    # Work with the Collection.
    print(f"Collection with ID {collection.metadata.collection_id} collected at {collection.metadata.timestamp}.")
    print(f"It has collected {collection.metadata.fleet_count} fleets and {len(collection.users)} players.")

    # You can use the Collection's ID in other methods, too, e.g. get the top 100 players at the end of the month.
    _, top_100_users = await client.get_top_100_users_from_collection(collection.metadata.collection_id)
    print(f"The player ranked 3rd last month was: {top_100_users[2].name}")

    # Or obtain the player stats of the 2nd best player last month over time
    user_history = await client.get_user_history(top_100_users[1].id, interval=ParameterInterval.MONTHLY)
    print(
        "Found %i history entries for player %s from %s to %s",
        len(user_history),
        top_100_users[1].name,
        user_history[0].collection.timestamp.isoformat(),
        user_history[-1].collection.timestamp.isoformat(),
    )

if __name__ == "__main__":
    asyncio.run(print_latest_tournament_results())
```
The library converts localized `datetime` objects to UTC or assumes UTC, if now `timezone` information is given. Any `datetime` objects returned are in UTC.

# ⚙️ Installation
**Python 3.11 or higher is required**

To install the latest version of this library, run the following command:
```sh
pip install -U pss-fleet-data-client
```

# 🖊️ Contribute
If you ran across a bug or have a feature request, please check if there's [already an issue](https://github.com/PSS-Tools-Development/pss-fleet-data-client/issues) for that and if not, [open a new one](https://github.com/PSS-Tools-Development/pss-fleet-data-client/issues/new).

If you want to fix a bug or add a feature, please check out the [Contribution Guide](CONTRIBUTING.md).

# 🆘 Support
If you need help using the library or want to contribute, you can join my support Discord at: [discord.gg/kKguSec](https://discord.gg/kKguSec)

# 🔗 Links
- Documentation (tbd)
- [Official Support Discord server](https://discord.gg/kKguSec)
- [PSS Fleet Data API](https://fleetdata.dolores2.xyz)
- [Buy me a can of cat food](https://buymeacoffee.com/the_worst_pss)
- [Or a coffee](https://ko-fi.com/theworstpss)
