from helpers import convert_txt_to_df
import pandas as pd

EVENT_CODE_PATH = './NBA Hackathon - Event Codes.txt'
GAME_LINEUP_DATA = './NBA Hackathon - Game Lineup Data Sample (50 Games).txt'
PLAY_BY_PLAY_DATA_PATH = './NBA Hackathon - Play by Play Data Sample (50 Games).txt'

SORT_ORDER = {
    'BY': ['Period', 'PC_Time', 'WC_Time', 'Event_Num'],
    'ASCENDING': [True, False, True, True]
}


def generate_data():
    event_code = convert_txt_to_df(EVENT_CODE_PATH)
    game_lineup = convert_txt_to_df(GAME_LINEUP_DATA)
    play_by_play = convert_txt_to_df(PLAY_BY_PLAY_DATA_PATH)

    all_games = play_by_play['Game_id'].unique()
    game_breakout_df = {}

    for game in all_games:
        if game:
            single_game_df = play_by_play.loc[play_by_play['Game_id'] == game]
            game_breakout_df[game] = single_game_df.sort_values(by=SORT_ORDER['BY'], ascending=SORT_ORDER['ASCENDING'])




generate_data()
