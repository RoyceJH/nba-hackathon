from helpers import convert_txt_to_df

EVENT_CODE_PATH = './NBA Hackathon - Event Codes.txt'
GAME_LOG_PATH = './NBA Hackathon - Game Lineup Data Sample (50 Games).txt'
PLAY_DATA_PATH = './NBA Hackathon - Play by Play Data Sample (50 Games).txt'


def generate_data():
    event_df = convert_txt_to_df(EVENT_CODE_PATH)
    game_log_df = convert_txt_to_df(GAME_LOG_PATH)
    play_data_df = convert_txt_to_df(PLAY_DATA_PATH)
