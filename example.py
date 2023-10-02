import datetime
import os
from typing import List

from src.client import PssTournamentDataClient


CLIENT_EMAIL: str = str(os.environ.get('GDRIVE_SERVICE_CLIENT_EMAIL'))
CLIENT_ID: str = str(os.environ.get('GDRIVE_SERVICE_CLIENT_ID'))
FOLDER_ID: str = '10wOZgAQk_0St2Y_jC3UW497LVpBNxWmP'
PRIVATE_KEY_ID: str = str(os.environ.get('GDRIVE_SERVICE_PRIVATE_KEY_ID'))
PRIVATE_KEY: str = str(os.environ.get('GDRIVE_SERVICE_PRIVATE_KEY'))
PROJECT_ID: str = str(os.environ.get('GDRIVE_SERVICE_PROJECT_ID'))
SERVICE_ACCOUNT_FILE: str = 'client_secrets.json'
SETTINGS_FILE: str = 'settings.yaml'
SCOPES: List[str] = ['https://www.googleapis.com/auth/drive']
TOURNAMENT_DATA_START_DATE: datetime.datetime = datetime.datetime(year=2019, month=10, day=9, hour=12)


def main() -> None:
    client = PssTournamentDataClient(FOLDER_ID, PRIVATE_KEY_ID, PRIVATE_KEY, CLIENT_EMAIL, CLIENT_ID, SCOPES, FOLDER_ID, SERVICE_ACCOUNT_FILE, SETTINGS_FILE, TOURNAMENT_DATA_START_DATE)
    print()
    
    tourney_data = client.get_latest_monthly_data()
    print('Trek Wolfpack Tournament data:')
    for fleet_data in tourney_data.get_fleet_data_by_name('Trek Wolf').values():
        print(fleet_data)
        break
    print()
    print('The worst. Tournament Data:')
    for user_data in tourney_data.get_user_data_by_name('The worst.').values():
        print(user_data)
        break


if __name__ == "__main__":
    main()
