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
