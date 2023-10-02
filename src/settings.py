import os as _os

MOST_RECENT_TOURNAMENT_DATA: bool = bool(int(_os.environ.get('MOST_RECENT_TOURNAMENT_DATA', 0)))
