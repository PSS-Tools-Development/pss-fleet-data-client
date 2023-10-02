import calendar
from datetime import datetime, timedelta, timezone
import json
import os
import random
from threading import Lock
import time
from typing import Dict, List, Optional, Tuple
import urllib.parse
import yaml

import pydrive.auth
import pydrive.drive
import pydrive.files

from . import settings
from . import utils
from .tourney_data import PssTournamentData


__all__ = [
    'TourneyDataClient',
]


# ---------- Classes ----------

class PssTournamentDataClient():
    def __init__(self, project_id: str, private_key_id: str, private_key: str, client_email: str, client_id: str, scopes: List[str], folder_id: str, service_account_file_path: str, settings_file_path: str, earliest_date: datetime) -> None:
        print('Create TourneyDataClient')
        self._client_email: str = client_email
        self._client_id: str = client_id
        self._folder_id: str = folder_id
        self._private_key: str = private_key
        self._private_key_id: str = private_key_id
        self._project_id: str = project_id
        self._scopes: List[str] = list(scopes)
        self._service_account_file_path: str = service_account_file_path
        self._settings_file_path: str = settings_file_path
        self.__earliest_date: datetime = earliest_date

        self.__READ_LOCK: Lock = Lock()
        self.__WRITE_LOCK: Lock = Lock()
        self.__write_requested: bool = False
        self.__reader_count: int = 0

        self.__cache: Dict[int, Dict[int, Dict[int, PssTournamentData]]] = {}

        self.__initialized = False
        self.__initialize()


    @property
    def from_month(self) -> int:
        return self.__earliest_date.month

    @property
    def from_year(self) -> int:
        return self.__earliest_date.year
    
    @property
    def to_day(self) -> int:
        return max(self.__cache.get(self.to_month, {}).keys())

    @property
    def to_month(self) -> int:
        return max(self.__cache.get(self.to_year, {}).keys())

    @property
    def to_year(self) -> int:
        return max(self.__cache.keys())


    def get_data(self, year: int, month: int, day: Optional[int] = None, initializing: bool = False) -> PssTournamentData:
        if year < self.from_year:
            raise ValueError(f'There\'s no data from {year}. Earliest data available is from {calendar.month_name[self.from_month]} {self.from_year}.')
        if year == self.from_year:
            if month < self.from_month:
                raise ValueError(f'There\'s no data from {calendar.month_name[month]} {year}. Earliest data available is from {calendar.month_name[self.from_month]} {self.from_year}.')
        if not initializing:
            if year > self.to_year or (year == self.to_year and month > self.to_month):
                utc_now = utils.get_utc_now()
                if utc_now.year == year and utc_now.month == month:
                    if day is None:
                        raise ValueError(f'There\'s no data from {calendar.month_name[month]} {year}. Most recent data available is from {calendar.month_name[self.to_month]} {self.to_year}.')
                    elif day >= utc_now.day:
                        raise ValueError(f'There\'s no data from {calendar.month_name[month]} {day}, {year}. Most recent data available is from {calendar.month_name[self.to_month]} {self.to_day}, {self.to_year}.')

        result = self.__read_data(year, month, day)

        if result is None:
            result = self.__retrieve_data(year, month, day, initializing=initializing)
            self.__cache_data(result)

        return result


    def get_latest_daily_data(self, initializing: bool = False) -> PssTournamentData:
        yesterday = utils.get_utc_now() - utils.ONE_DAY
        result = self.get_data(yesterday.year, yesterday.month, yesterday.day, initializing=initializing)
        return result


    def get_latest_monthly_data(self, initializing: bool = False) -> PssTournamentData:
        utc_now = utils.get_utc_now()
        year, month = PssTournamentDataClient.__get_last_tourney_year_and_month(utc_now)
        if settings.MOST_RECENT_TOURNAMENT_DATA:
            month += 1
            if month == 13:
                month = 1
                year += 1
        result = None
        while year > self.from_year or month >= self.from_month:
            result = self.get_data(year, month, initializing=initializing)
            if result:
                break
            month -= 1
            if month == 0:
                year -= 1
                month = 12
        return result


    def get_second_latest_daily_data(self, initializing: bool = False) -> PssTournamentData:
        yesterday = utils.get_utc_now() - utils.ONE_DAY - utils.ONE_DAY
        result = self.get_data(yesterday.year, yesterday.month, yesterday.day, initializing=initializing)
        return result


    def __add_reader(self) -> None:
        with self.__READ_LOCK:
            self.__reader_count = self.__reader_count + 1


    def __assert_initialized(self) -> None:
        if self.__drive is None:
            raise Exception('The __drive object has not been initialized, yet!')


    def __cache_data(self, tourney_data: PssTournamentData) -> bool:
        if tourney_data:
            self.__request_write()
            can_write = False
            while not can_write:
                can_write = self.__get_reader_count() == 0
                if not can_write:
                    time.sleep(random.random())
                with self.__WRITE_LOCK:
                    self.__cache.setdefault(tourney_data.year, {}).setdefault(tourney_data.month, {})[tourney_data.day] = tourney_data
                    self.__write_requested = False
                return True
            return False
        return False


    def __ensure_initialized(self) -> None:
        try:
            self.__drive.ListFile({'q': f'\'{self._folder_id}\' in parents and title contains \'highaöegjoyödfmj giod\''}).GetList()
        except pydrive.auth.InvalidConfigError:
            self.__initialize()


    def __get_first_file(self, file_name: str) -> pydrive.files.GoogleDriveFile:
        file_list = self.__drive.ListFile({'q': f"'{self._folder_id}' in parents and title = '{file_name}'"}).GetList()
        for file_def in file_list:
            return file_def
        return None


    def __get_latest_file(self, year: int, month: int, day: Optional[int] = None, initializing: bool = False) -> pydrive.files.GoogleDriveFile:
        if not initializing:
            self.__ensure_initialized()
        file_name_part: str = f'{year:04d}{month:02d}'
        if day is not None:
            file_name_part += f'{day:02d}'
        file_list = self.__drive.ListFile({'q': f'\'{self._folder_id}\' in parents and title contains \'pss-top-100_{file_name_part}\''}).GetList()
        if file_list:
            file_list = sorted(file_list, key=lambda f: f['title'], reverse=True)
            return file_list[0]
        return None


    def __get_reader_count(self) -> int:
        with self.__READ_LOCK:
            result = self.__reader_count
        return result


    def __get_write_requested(self) -> bool:
        with self.__WRITE_LOCK:
            result = self.__write_requested
        return result


    def __initialize(self) -> None:
        PssTournamentDataClient.create_service_account_credential_json(self._project_id, self._private_key_id, self._private_key, self._client_email, self._client_id, self._service_account_file_path)
        PssTournamentDataClient.create_service_account_settings_yaml(self._settings_file_path, self._service_account_file_path, self._scopes)
        self.__gauth: pydrive.auth.GoogleAuth = pydrive.auth.GoogleAuth(settings_file=self._settings_file_path)
        credentials = pydrive.auth.ServiceAccountCredentials.from_json_keyfile_name(self._service_account_file_path, self._scopes)
        self.__gauth.credentials = credentials
        self.__drive: pydrive.drive.GoogleDrive = pydrive.drive.GoogleDrive(self.__gauth)
        self.get_latest_monthly_data(initializing=True)
        self.get_latest_daily_data(initializing=True)
        self.get_second_latest_daily_data(initializing=True)
        self.__initialized = True


    def __read_data(self, year: int, month: int, day: Optional[int] = None) -> PssTournamentData:
        can_read = False
        while not can_read:
            can_read = not self.__get_write_requested()
            if not can_read:
                time.sleep(random.random())

        self.__add_reader()
        result = self.__cache.get(year, {}).get(month, {})
        if result:
            if day is None:
                result = result.get(max(result.keys()), None)
            else:
                result = result.get(day, None)
        else:
            result = None
        self.__remove_reader()
        return result


    def __remove_reader(self) -> None:
        with self.__READ_LOCK:
            self.__reader_count = self.__reader_count - 1


    def __request_write(self) -> None:
        with self.__WRITE_LOCK:
            self.__write_requested = True


    def __retrieve_data(self, year: int, month: int, day: Optional[int] = False, initializing: bool = False) -> PssTournamentData:
        if not initializing:
            self.__ensure_initialized()
        g_file = self.__get_latest_file(year, month, day, initializing=initializing)
        result = None
        if g_file:
            raw_data = g_file.GetContentString()
            data = json.loads(raw_data)
            if data:
                result = PssTournamentData(data)
        return result


    @staticmethod
    def create_service_account_credential_json(project_id: str, private_key_id: str, private_key: str, client_email: str, client_id: str, service_account_file_path: str) -> None:
        if os.path.exists(service_account_file_path):
            print(f'Using existing service account connection file at: {service_account_file_path}')
            return
        
        contents = {
            'type': 'service_account',
            'project_id': project_id,
            'private_key_id': private_key_id,
            'private_key': private_key,
            'client_email': client_email,
            'client_id': client_id,
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
            'client_x509_cert_url': f'https://www.googleapis.com/robot/v1/metadata/x509/{urllib.parse.quote(client_email)}',
        }
        with open(service_account_file_path, 'w+') as service_file:
            json.dump(contents, service_file, indent=2)
        print(f'Created service account connection file at: {service_account_file_path}')


    @staticmethod
    def create_service_account_settings_yaml(settings_file_path: str, service_account_file_path: str, scopes: List[str]) -> None:
        if not os.path.isfile(settings_file_path):
            contents = {}
            contents['client_config_backend'] = 'file'
            contents['client_config_file'] = service_account_file_path
            contents['save_credentials'] = True
            contents['save_credentials_backend'] = 'file'
            contents['save_credentials_file'] = 'credentials.json'
            contents['oauth_scope'] = scopes

            with open(settings_file_path, 'w+') as settings_file:
                yaml.dump(contents, settings_file)
            print(f'Created settings yaml file at: {settings_file_path}')


    @staticmethod
    def __fix_filename_datetime(dt: datetime) -> datetime:
        dt = datetime(dt.year, dt.month, 1, tzinfo=timezone.utc)
        dt = dt - timedelta(minutes=1)
        return dt


    @staticmethod
    def __get_latest_file_name(dt: datetime) -> str:
        dt = PssTournamentDataClient.__fix_filename_datetime(dt)
        timestamp = dt.strftime('%Y%m%d-%H%M%S')
        result = f'pss-top-100_{timestamp}.json'
        return result


    @staticmethod
    def __get_last_tourney_year_and_month(dt: datetime) -> Tuple[int, int]:
        dt = PssTournamentDataClient.__fix_filename_datetime(dt)
        return dt.year, dt.month


    @staticmethod
    def retrieve_past_day_month_year(month: str, year: str, utc_now: datetime) -> Tuple[int, int]:
        if not utc_now:
            utc_now = utils.get_utc_now()

        if month is None:
            temp_month = utc_now.month - 1
            if not settings.MOST_RECENT_TOURNAMENT_DATA:
                temp_month -= 1
            temp_month = temp_month % 12 + 1
        else:
            month = str(month)
            temp_month = utils.MONTH_NAME_TO_NUMBER.get(month.lower(), None)
            temp_month = temp_month or utils.MONTH_SHORT_NAME_TO_NUMBER.get(month.lower(), None)
            if temp_month is None:
                try:
                    temp_month = int(month)
                except:
                    raise ValueError(f'Parameter month got an invalid value: {month}')
        if year is None:
            year = utc_now.year
            if utc_now.month + (1 if settings.MOST_RECENT_TOURNAMENT_DATA else 0) <= temp_month:
                year -= 1
        year = int(year)
        _, day = calendar.monthrange(year, temp_month)
        return day, temp_month, int(year)