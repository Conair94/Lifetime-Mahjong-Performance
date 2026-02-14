import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data.csv')
README_PATH = os.path.join(os.path.dirname(BASE_DIR), 'README.md')
STATS_CSV_PATH = os.path.join(BASE_DIR, 'player_stats.csv')
BETTING_ODDS_PATH = os.path.join(os.path.dirname(BASE_DIR), 'Gambling and Forecasting', 'Betting_Odds.md')
PROCESSED_NIGHT_COUNT_PATH = os.path.join(os.path.dirname(BASE_DIR), 'Gambling and Forecasting', 'processed_night_count.txt')

# Player Lists
BIG3 = ['connor', 'helio', 'sam']
GUESTS = ['oscar', 'nick', 'drew', 'ruohan', 'brandon', 'lixin', 'alice', 'eileen']

# Betting Configuration
HOUSE_EDGE = 1.10
FAN_THRESHOLD = 15.5
