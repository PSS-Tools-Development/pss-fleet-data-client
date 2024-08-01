import asyncio
from datetime import datetime, timezone

from pss_fleet_data import ParameterInterval, PssFleetDataClient, utils


client = PssFleetDataClient(base_url="https://fleetdata.dolores2.xyz")


async def print_latest_tournament_results():
    most_recent_timestamp = utils.get_most_recent_timestamp(datetime.now(tz=timezone.utc), ParameterInterval.MONTHLY)  #
    collection = await client.get_most_recent_collection_by_timestamp(most_recent_timestamp)
    print(f"Collection with ID {collection.metadata.collection_id} collected at {collection.metadata.timestamp}.")
    print(f"It has collected {collection.metadata.fleet_count} fleets and {len(collection.users)} players.")


if __name__ == "__main__":
    asyncio.run(print_latest_tournament_results())
