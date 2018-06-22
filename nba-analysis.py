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

    convert_cols_to_int(event_code, NUMERICAL_COLUMNS)
    convert_cols_to_int(play_by_play, NUMERICAL_COLUMNS)
    convert_cols_to_int(game_lineup, NUMERICAL_COLUMNS)


    all_games = play_by_play['Game_id'].unique()

    for game in all_games:
        if game:
            single_game = play_by_play.loc[play_by_play['Game_id'] == game]
            # Sorting purely based on WC_Time might have the same output
            single_game = single_game.sort_values(SORT_ORDER['BY'], ascending=SORT_ORDER['ASCENDING'])
            player_contributions = calculate_adv_stats(single_game, event_code, game_lineup)


def calculate_adv_stats(game, event_code, game_lineup):
    player_breakdown = {}
    on_court_players = {}
    game_id = game['Game_id'][0]
    halt_player_change = False
    delayed_substitution = {}

    # get_start_period_players(on_court_players, game_lineup, game['Game_id'][0], 1)

    for _, play in game.iterrows():
        _, _, event_description, action_description = lookup_event(event_code, play)

        if 'Start Period' in event_description:
            get_start_period_players(on_court_players, game_lineup, game_id, play['Period'])
        elif 'Foul' in event_description:
            halt_player_change = True
        elif 'Made Shot' in event_description:
            points = play['Option1']
            scoring_team = play['Team_id']
            stats_to_update = calculate_stats_to_update(on_court_players, points, scoring_team)
            update_stats(player_breakdown, stats_to_update)

def update_stats(player_breakdown, stats_to_update):
    for player, points in stats_to_update.items():
        try:
            player_breakdown[player]
        except:
            player_breakdown[player] = 0

        player_breakdown[player] += points
        print('hi')


def calculate_stats_to_update(on_court_players, points, scoring_team):
    stat_update = {}

    for team in on_court_players:
        if team == scoring_team:
            for player in on_court_players[team]:
                stat_update[player] = points
        else:
            for player in on_court_players[team]:
                stat_update[player] = -points

    return stat_update



def get_start_period_players(on_court_players, game_lineup, game_id, period):
    period_starting_lineup = game_lineup.loc[
        (game_lineup['Game_id'] == game_id) & (game_lineup['Period'] == period)
    ]
    for _, player in period_starting_lineup.iterrows():
        try:
            on_court_players[player['Team_id']].append(player['Person_id'])
        except:
            on_court_players[player['Team_id']] = [player['Person_id']]


def lookup_event(event_code, play):
    event = event_code.loc[
        (event_code['"Event_Msg_Type"'] == play['Event_Msg_Type']) & (event_code['"Action_Type"'] == play['Action_Type'])
    ]
    return event.values.flatten()




generate_data()
