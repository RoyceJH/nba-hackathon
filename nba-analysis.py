from helpers import convert_txt_to_df, convert_cols_to_int

EVENT_CODE_PATH = './NBA Hackathon - Event Codes.txt'
GAME_LINEUP_DATA = './NBA Hackathon - Game Lineup Data Sample (50 Games).txt'
PLAY_BY_PLAY_DATA_PATH = './NBA Hackathon - Play by Play Data Sample (50 Games).txt'

SORT_ORDER = {
    'BY': ['Period', 'PC_Time', 'WC_Time', 'Event_Num'],
    'ASCENDING': [True, False, True, True]
}

NUMERICAL_COLUMNS = [
    'Period', 'PC_Time', 'WC_Time', 'Event_Num', 'Event_Msg_Type', 'Action_Type', 'Option1', 'Option2', 'Option3',
    'Team_id_type'
]


def generate_data():
    event_code = convert_txt_to_df(EVENT_CODE_PATH)
    game_lineup = convert_txt_to_df(GAME_LINEUP_DATA)
    play_by_play = convert_txt_to_df(PLAY_BY_PLAY_DATA_PATH)

    convert_cols_to_int(play_by_play, NUMERICAL_COLUMNS)

    all_games = play_by_play['Game_id'].unique()

    for game in all_games:
        if game:
            single_game = play_by_play.loc[play_by_play['Game_id'] == game]
            # Sorting purely based on WC_Time might have the same output
            single_game = single_game.sort_values(SORT_ORDER['BY'], ascending=SORT_ORDER['ASCENDING'])
            player_contributions = calculate_adv_stats(single_game)


def calculate_adv_stats(game):
    print('hi')




generate_data()
