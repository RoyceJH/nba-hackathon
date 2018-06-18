from helpers import convert_txt_to_df
import pandas as pd

EVENT_CODE_PATH = './NBA Hackathon - Event Codes.txt'
GAME_LINEUP_DATA = './NBA Hackathon - Game Lineup Data Sample (50 Games).txt'
PLAY_BY_PLAY_DATA_PATH = './NBA Hackathon - Play by Play Data Sample (50 Games).txt'


def generate_data():
    event_code = convert_txt_to_df(EVENT_CODE_PATH)
    game_lineup = convert_txt_to_df(GAME_LINEUP_DATA)
    play_by_play = convert_txt_to_df(PLAY_BY_PLAY_DATA_PATH)

    play_by_play.set_index('Game_id', inplace=True)
    game_breakout = {}
    print('hi')

    for game_id, play in play_by_play.iterrows():
        print((game_id, play))



generate_data()
