from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union


from . import lookups
from . import utils
from .typehints import EntitiesData, EntityInfo


__all__ = [
    'TourneyData',
]


# ---------- Classes ----------

class PssTournamentData(object):
    def __init__(self, data: dict) -> None:
        self.__fleets: EntitiesData = None
        self.__users: EntitiesData = None
        self.__meta: Dict[str, object] = data['meta']

        if not self.__meta.get('schema_version', None):
            self.__meta['schema_version'] = 3
        
        if self.__meta['schema_version'] >= 9:
            self.__fleets = PssTournamentData.__create_fleet_data_from_data_v7(data['fleets'], data['users']) # No change to prior schema version
            self.__users = PssTournamentData.__create_user_dict_from_data_v9(data['users'], self.__fleets)
        elif self.__meta['schema_version'] >= 8:
            self.__fleets = PssTournamentData.__create_fleet_data_from_data_v7(data['fleets'], data['users']) # No change to prior schema version
            self.__users = PssTournamentData.__create_user_dict_from_data_v8(data['users'], self.__fleets)
        elif self.__meta['schema_version'] >= 7:
            self.__fleets = PssTournamentData.__create_fleet_data_from_data_v7(data['fleets'], data['users'])
            self.__users = PssTournamentData.__create_user_dict_from_data_v6(data['users'], self.__fleets) # No change to prior schema version
        elif self.__meta['schema_version'] >= 6:
            self.__fleets = PssTournamentData.__create_fleet_data_from_data_v6(data['fleets'], data['users'])
            self.__users = PssTournamentData.__create_user_dict_from_data_v6(data['users'], self.__fleets)
        elif self.__meta['schema_version'] >= 5:
            self.__fleets = PssTournamentData.__create_fleet_data_from_data_v4(data['fleets'], data['users']) # No change to prior schema version
            self.__users = PssTournamentData.__create_user_dict_from_data_v5(data['users'], self.__fleets)
        elif self.__meta['schema_version'] >= 4:
            self.__fleets = PssTournamentData.__create_fleet_data_from_data_v4(data['fleets'], data['users'])
            self.__users = PssTournamentData.__create_user_dict_from_data_v4(data['users'], self.__fleets)
        elif self.__meta['schema_version'] >= 3:
            self.__fleets = PssTournamentData.__create_fleet_data_from_data_v3(data['fleets'], data['users'], data['data'])
            self.__users = PssTournamentData.__create_user_data_from_data_v3(data['users'], data['data'], self.__fleets)
        self.__data_date: datetime = utils.parse_formatted_datetime(data['meta']['timestamp'], include_tz=False, include_tz_brackets=False)

        self.__top_100_users: EntitiesData = {}
        top_users_infos = sorted(list(self.__users.values()), key=lambda user_info: -int(user_info.get('Trophy', 0)))[:100]
        top_users_ids = [user_info['Id'] for user_info in top_users_infos]
        for key, value in self.__users.items():
            if key in top_users_ids:
                self.__top_100_users[key] = value
                top_users_ids.remove(key)
                if not top_users_ids:
                    break


    @property
    def collected_in(self) -> float:
        """
        Number of seconds it took to collect the data.
        """
        return self.__meta['duration']

    @property
    def day(self) -> int:
        """
        Short for data_date.day
        """
        return self.__data_date.day

    @property
    def fleet_ids(self) -> List[str]:
        return list(self.__fleets.keys())

    @property
    def fleets(self) -> EntitiesData:
        """
        Copy of fleet data
        """
        return dict({key: dict(value) for key, value in self.__fleets.items()})

    @property
    def max_tournament_battle_attempts(self) -> Optional[int]:
        """
        The maximum number of tournament battle attempts for a day.
        """
        result = self.__meta.get('max_tournament_battle_attempts')
        if result:
            return int(result)
        return None

    @property
    def month(self) -> int:
        """
        Short for data_date.month
        """
        return self.__data_date.month

    @property
    def retrieved_at(self) -> datetime:
        """
        Point in time when the data collection started.
        """
        return self.__data_date

    @property
    def schema_version(self) -> int:
        """
        Data collection schema version. Use to determine which information is available for fleets and users.
        """
        return self.__meta['schema_version']

    @property
    def top_100_users(self) -> EntitiesData:
        """
        Copy of top 100 users
        """
        return dict({key: dict(value) for key, value in self.__top_100_users.items()})

    @property
    def user_ids(self) -> List[str]:
        return list(self.__users.keys())

    @property
    def users(self) -> EntitiesData:
        """
        Copy of user data
        """
        return dict({key: dict(value) for key, value in self.__users.items()})

    @property
    def year(self) -> int:
        """
        Short for data_date.year
        """
        return self.__data_date.year


    def get_fleet_data_by_id(self, fleet_id: str) -> EntityInfo:
        """
        Look up fleet by id
        """
        return dict(self.__fleets.get(fleet_id, None))


    def get_fleet_data_by_name(self, fleet_name: str) -> EntitiesData:
        """
        Looks up fleets having the specified fleet_name in their name.
        Case-insensitive.
        """
        result = {}
        for current_fleet_id, current_fleet_data in self.__fleets.items():
            current_fleet_name = current_fleet_data.get('AllianceName', current_fleet_data.get('Name', ''))
            if current_fleet_name and fleet_name.lower() in current_fleet_name.lower():
                result[current_fleet_id] = dict(current_fleet_data)
        return result


    def get_user_data_by_id(self, user_id: str) -> EntityInfo:
        """
        Look up user by id
        """
        return dict(self.__users.get(user_id, None))


    def get_user_data_by_name(self, user_name: str) -> EntitiesData:
        """
        Looks up users having the specified user_name in their name.
        Case-insensitive.
        """
        result = {}
        for current_user_id, current_user_data in self.__users.items():
            current_user_name = current_user_data.get('Name', None)
            if current_user_name and user_name.lower() in current_user_name.lower():
                result[current_user_id] = dict(current_user_data)
        return result


    @staticmethod
    def __create_fleet_data_from_data_v3(fleets_data: List[List[Union[int, str]]], users_data: List[List[Union[int, str]]], data: List[List[Union[int, str]]]) -> EntitiesData:
        result = {}
        for i, entry in enumerate(fleets_data, 1):
            alliance_id = entry[0]
            users = [user_info for user_info in data if user_info[1] == alliance_id]
            if len(entry) == 4:
                division_design_id = entry[3]
            else:
                if i > 50:
                    division_design_id = '4'
                elif i > 20:
                    division_design_id = '3'
                elif i > 8:
                    division_design_id = '2'
                else:
                    division_design_id = '1'
            result[alliance_id] = {
                'AllianceId': alliance_id,
                'AllianceName': entry[1],
                'Score': entry[2],
                'DivisionDesignId': division_design_id,
                'NumberOfMembers': len(users),
            }
        ranked_fleets_infos = sorted(sorted(result.values(), key=lambda fleet_info: int(fleet_info['Score']), reverse=True), key=lambda fleet_info: fleet_info['DivisionDesignId'])
        for i, ranked_fleet_info in enumerate(ranked_fleets_infos, 1):
            result[ranked_fleet_info['AllianceId']]['Ranking'] = str(i)
        return result


    @staticmethod
    def __create_fleet_data_from_data_v4(fleets_data: List[List[Union[int, str]]], users_data: List[List[Union[int, str]]]) -> EntitiesData:
        result = {}
        for i, entry in enumerate(fleets_data, 1):
            alliance_id = str(entry[0])
            users = [user_info for user_info in users_data if user_info[2] == entry[0]]
            result[alliance_id] = {
                'AllianceId': alliance_id,
                'AllianceName': entry[1],
                'Score': str(entry[2]),
                'DivisionDesignId': str(entry[3]),
                'Trophy': str(entry[4]),
                'NumberOfMembers': len(users),
            }
        ranked_fleets_infos = sorted(result.values(), key=lambda fleet_info: (fleet_info['DivisionDesignId'], -int(fleet_info['Score']), -int(fleet_info['Trophy'])))
        for i, ranked_fleet_info in enumerate(ranked_fleets_infos, 1):
            result[ranked_fleet_info['AllianceId']]['Ranking'] = str(i)
        return result


    @staticmethod
    def __create_fleet_data_from_data_v6(fleets_data: List[List[Union[int, str]]], users_data: List[List[Union[int, str]]]) -> EntitiesData:
        result = {}
        for i, entry in enumerate(fleets_data, 1):
            alliance_id = str(entry[0])
            users = [user_info for user_info in users_data if user_info[2] == entry[0]]
            result[alliance_id] = {
                'AllianceId': alliance_id,
                'AllianceName': entry[1],
                'Score': str(entry[2]),
                'DivisionDesignId': str(entry[3]),
                'Trophy': str(entry[4]),
                'NumberOfMembers': len(users),
                'ChampionshipScore': str(entry[5]),
            }
        ranked_fleets_infos = sorted(result.values(), key=lambda fleet_info: (fleet_info['DivisionDesignId'], -int(fleet_info['Score']), -int(fleet_info['Trophy'])))
        for i, ranked_fleet_info in enumerate(ranked_fleets_infos, 1):
            result[ranked_fleet_info['AllianceId']]['Ranking'] = str(i)
        return result


    @staticmethod
    def __create_fleet_data_from_data_v7(fleets_data: List[List[Union[int, str]]], users_data: List[List[Union[int, str]]]) -> EntitiesData:
        result = {}
        for i, entry in enumerate(fleets_data, 1):
            alliance_id = str(entry[0])
            users = [user_info for user_info in users_data if user_info[2] == entry[0]]
            result[alliance_id] = {
                'AllianceId': alliance_id,
                'AllianceName': entry[1],
                'Score': str(entry[2]),
                'DivisionDesignId': str(entry[3]),
                'Trophy': str(entry[4]),
                'NumberOfMembers': len(users) if users else str(entry[6]),
                'ChampionshipScore': str(entry[5]),
                'NumberOfApprovedMembers': str(entry[7])
            }
        ranked_fleets_infos = sorted(result.values(), key=lambda fleet_info: (fleet_info['DivisionDesignId'], -int(fleet_info['Score']), -int(fleet_info['Trophy'])))
        for i, ranked_fleet_info in enumerate(ranked_fleets_infos, 1):
            result[ranked_fleet_info['AllianceId']]['Ranking'] = str(i)
        return result




    @staticmethod
    def __create_user_data_from_data_v3(users: List[List[Union[int, str]]], data: List[List[Union[int, str]]], fleet_data: EntitiesData) -> EntitiesData:
        result = {}
        users_dict = dict(users)
        for entry in data:
            fleet_id = entry[1]
            result[entry[0]] = {
                'Id': entry[0],
                'AllianceId': fleet_id,
                'Trophy': entry[2],
                'AllianceScore': entry[3],
                'AllianceMembership': entry[4],
                'AllianceJoinDate': entry[5],
                'LastLoginDate': entry[6],
                'Name': users_dict[entry[0]],
                'Alliance': {}
            }
            if fleet_id and fleet_id != '0':
                fleet_info: EntityInfo = fleet_data.get(fleet_id, {})
                for key, value in fleet_info.items():
                    result[entry[0]]['Alliance'][key] = value

        return result


    @staticmethod
    def __create_user_dict_from_data_v4(users: List[List[Union[int, str]]], fleet_data: EntitiesData) -> EntitiesData:
        result = {}
        for user in users:
            fleet_id = str(user[2])
            user_id = str(user[0])
            result[user_id] = {
                'Id': user_id,
                'AllianceId': fleet_id,
                'Trophy': str(user[3]),
                'AllianceScore': str(user[4]),
                'AllianceMembership': lookups.ALLIANCE_MEMBERSHIP_LOOKUP[user[5]],
                'Name': user[1],
                'CrewDonated': str(user[9]),
                'CrewReceived': str(user[10]),
                'PVPAttackWins': str(user[11]),
                'PVPAttackLosses': str(user[12]),
                'PVPAttackDraws': str(user[13]),
                'PVPDefenceWins': str(user[14]),
                'PVPDefenceLosses': str(user[15]),
                'PVPDefenceDraws': str(user[16]),
                'Alliance': {}
            }
            if fleet_id and fleet_id != '0':
                fleet_info = fleet_data.get(fleet_id, {})
                for key, value in fleet_info.items():
                    result[user_id]['Alliance'][key] = value

        return result


    @staticmethod
    def __create_user_dict_from_data_v5(users: List[List[Union[int, str]]], fleet_data: EntitiesData) -> EntitiesData:
        result = {}
        for user in users:
            fleet_id = str(user[2])
            user_id = str(user[0])
            result[user_id] = {
                'Id': user_id,
                'AllianceId': fleet_id,
                'Trophy': str(user[3]),
                'AllianceScore': str(user[4]),
                'AllianceMembership': lookups.ALLIANCE_MEMBERSHIP_LOOKUP[user[5]],
                'AllianceJoinDate': PssTournamentData.__convert_timestamp_v4(user[6]) if user[6] else None,
                'LastLoginDate': PssTournamentData.__convert_timestamp_v4(user[7]),
                'Name': user[1],
                'LastHeartBeatDate': PssTournamentData.__convert_timestamp_v4(user[8]),
                'CrewDonated': str(user[9]),
                'CrewReceived': str(user[10]),
                'PVPAttackWins': str(user[11]),
                'PVPAttackLosses': str(user[12]),
                'PVPAttackDraws': str(user[13]),
                'PVPDefenceWins': str(user[14]),
                'PVPDefenceLosses': str(user[15]),
                'PVPDefenceDraws': str(user[16]),
                'Alliance': {}
            }
            if fleet_id and fleet_id != '0':
                fleet_info = fleet_data.get(fleet_id, {})
                for key, value in fleet_info.items():
                    result[user_id]['Alliance'][key] = value

        return result


    @staticmethod
    def __create_user_dict_from_data_v6(users: List[List[Union[int, str]]], fleet_data: EntitiesData) -> EntitiesData:
        result = {}
        for user in users:
            fleet_id = str(user[2])
            user_id = str(user[0])
            result[user_id] = {
                'Id': user_id,
                'AllianceId': fleet_id,
                'Trophy': str(user[3]),
                'AllianceScore': str(user[4]),
                'AllianceMembership': lookups.ALLIANCE_MEMBERSHIP_LOOKUP[user[5]],
                'AllianceJoinDate': PssTournamentData.__convert_timestamp_v4(user[6]) if user[6] else None,
                'LastLoginDate': PssTournamentData.__convert_timestamp_v4(user[7]),
                'Name': user[1],
                'LastHeartBeatDate': PssTournamentData.__convert_timestamp_v4(user[8]),
                'CrewDonated': str(user[9]),
                'CrewReceived': str(user[10]),
                'PVPAttackWins': str(user[11]),
                'PVPAttackLosses': str(user[12]),
                'PVPAttackDraws': str(user[13]),
                'PVPDefenceWins': str(user[14]),
                'PVPDefenceLosses': str(user[15]),
                'PVPDefenceDraws': str(user[16]),
                'ChampionshipScore': str(user[17]),
                'Alliance': {}
            }
            if fleet_id and fleet_id != '0':
                fleet_info = fleet_data.get(fleet_id, {})
                for key, value in fleet_info.items():
                    result[user_id]['Alliance'][key] = value

        return result


    @staticmethod
    def __create_user_dict_from_data_v8(users: List[List[Union[int, str]]], fleet_data: EntitiesData) -> EntitiesData:
        result = {}
        for user in users:
            fleet_id = str(user[2])
            user_id = str(user[0])
            result[user_id] = {
                'Id': user_id,
                'AllianceId': fleet_id,
                'Trophy': str(user[3]),
                'AllianceScore': str(user[4]),
                'AllianceMembership': lookups.ALLIANCE_MEMBERSHIP_LOOKUP[user[5]],
                'AllianceJoinDate': PssTournamentData.__convert_timestamp_v4(user[6]) if user[6] else None,
                'LastLoginDate': PssTournamentData.__convert_timestamp_v4(user[7]),
                'Name': user[1],
                'LastHeartBeatDate': PssTournamentData.__convert_timestamp_v4(user[8]),
                'CrewDonated': str(user[9]),
                'CrewReceived': str(user[10]),
                'PVPAttackWins': str(user[11]),
                'PVPAttackLosses': str(user[12]),
                'PVPAttackDraws': str(user[13]),
                'PVPDefenceWins': str(user[14]),
                'PVPDefenceLosses': str(user[15]),
                'PVPDefenceDraws': str(user[16]),
                'ChampionshipScore': str(user[17]),
                'HighestTrophy': str(user[18]),
                'Alliance': {}
            }
            if fleet_id and fleet_id != '0':
                fleet_info = fleet_data.get(fleet_id, {})
                for key, value in fleet_info.items():
                    result[user_id]['Alliance'][key] = value

        return result


    @staticmethod
    def __create_user_dict_from_data_v9(users: List[List[Union[int, str]]], fleet_data: EntitiesData) -> EntitiesData:
        result = {}
        for user in users:
            fleet_id = str(user[2])
            user_id = str(user[0])
            result[user_id] = {
                'Id': user_id,
                'AllianceId': fleet_id,
                'Trophy': str(user[3]),
                'AllianceScore': str(user[4]),
                'AllianceMembership': lookups.ALLIANCE_MEMBERSHIP_LOOKUP[user[5]],
                'AllianceJoinDate': PssTournamentData.__convert_timestamp_v4(user[6]) if user[6] else None,
                'LastLoginDate': PssTournamentData.__convert_timestamp_v4(user[7]),
                'Name': user[1],
                'LastHeartBeatDate': PssTournamentData.__convert_timestamp_v4(user[8]),
                'CrewDonated': str(user[9]),
                'CrewReceived': str(user[10]),
                'PVPAttackWins': str(user[11]),
                'PVPAttackLosses': str(user[12]),
                'PVPAttackDraws': str(user[13]),
                'PVPDefenceWins': str(user[14]),
                'PVPDefenceLosses': str(user[15]),
                'PVPDefenceDraws': str(user[16]),
                'ChampionshipScore': str(user[17]),
                'HighestTrophy': str(user[18]),
                'TournamentBonusScore': str(user[19]),
                'Alliance': {}
            }
            if fleet_id and fleet_id != '0':
                fleet_info = fleet_data.get(fleet_id, {})
                for key, value in fleet_info.items():
                    result[user_id]['Alliance'][key] = value

        return result


    @staticmethod
    def __convert_timestamp_v4(timestamp: int) -> str:
        minutes, seconds = divmod(timestamp, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        td = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        dt = utils.PSS_START_DATETIME + td
        result = utils.format_pss_datetime(dt)
        return result