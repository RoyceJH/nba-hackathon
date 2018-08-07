from datetime import datetime

from helpers import convert_txt_to_df, convert_cols_to_int, create_workbook, setup_worksheet, add_dict_to_worksheet, \
    get_time_diff
from constants import START_PERIOD, SUBSTITUTION, SORT_ORDER, NUMERICAL_COLUMNS
from event_checkers import is_foul, is_delayed_sub_over, is_scoring_play, lookup_event

EVENT_CODE_PATH = './NBA Hackathon - Event Codes.txt'
GAME_LINEUP_DATA = './NBA Hackathon - Game Lineup Data Sample (50 Games).txt'
PLAY_BY_PLAY_DATA_PATH = './NBA Hackathon - Play by Play Data Sample (50 Games).txt'


def generate_data():
    event_code = convert_txt_to_df(EVENT_CODE_PATH)
    game_lineup = convert_txt_to_df(GAME_LINEUP_DATA)
    play_by_play = convert_txt_to_df(PLAY_BY_PLAY_DATA_PATH)

    convert_cols_to_int(event_code, NUMERICAL_COLUMNS)
    convert_cols_to_int(play_by_play, NUMERICAL_COLUMNS)
    convert_cols_to_int(game_lineup, NUMERICAL_COLUMNS)

    all_games = play_by_play['Game_id'].unique()

    workbook = create_workbook()
    worksheet = setup_worksheet(workbook)
    curr_row = 1

    for game in all_games:
        if game:
            single_game = play_by_play[play_by_play['Game_id'] == game]
            # Sorting purely based on WC_Time might have the same output
            single_game = single_game.sort_values(SORT_ORDER['BY'], ascending=SORT_ORDER['ASCENDING'])
            player_contribution_dict = calculate_adv_stats(single_game, event_code, game_lineup)
            curr_row = add_dict_to_worksheet(worksheet, player_contribution_dict, game, curr_row)

    workbook.close()


def calculate_adv_stats(game, event_code, game_lineup):
    player_breakdown = {}
    on_court_players = {}
    game_id = game['Game_id'].iloc[0]
    halt_player_change = False
    delayed_subs = {'leaving': [], 'incoming': []}
    start_time = datetime.now()
    print('Calculating stats for game: {}'.format(game_id))

    for _, play in game.iterrows():
        try:
            _, _, event_description, action_description = lookup_event(event_code, play)
        except ValueError:
            # There is a play with invalid Event msg type and Action type, let's skip over it
            continue

        if halt_player_change and is_delayed_sub_over(event_description):
            # When a shot attempt is made, we can assume Foul proceedings are over
            # First thing to check so that points aren't incorrectly attributed
            halt_player_change = False

            # Should be the same number of incoming and outgoing players and indexed by the same team
            for idx in range(len(delayed_subs['leaving'])):
                replace_players(on_court_players, delayed_subs['leaving'][idx], delayed_subs['incoming'][idx])

            delayed_subs = reset_delayed_substitutions()

        if is_foul(event_description):
            # As soon as foul occurs, subbing should be postponed for scoring purposes
            halt_player_change = True

        if START_PERIOD in event_description:
            set_start_period_players(on_court_players, game_lineup, game_id, play['Period'])
        elif is_scoring_play(event_description, action_description):
            points = play['Option1']
            scoring_team = play['Team_id']
            stats_to_update = calculate_stats_to_update(on_court_players, points, scoring_team)
            update_stats(player_breakdown, stats_to_update)
        elif SUBSTITUTION in event_description:
            if halt_player_change:
                delayed_subs['leaving'].append(play['Person1'])
                delayed_subs['incoming'].append(play['Person2'])
            else:
                leaving_player = play['Person1']
                incoming_player = play['Person2']
                replace_players(on_court_players, leaving_player, incoming_player)

    end_time = datetime.now()
    print('Finished calculating stats for game: {} in {} ms'.format(game_id, get_time_diff(start_time, end_time)))
    return player_breakdown


def update_stats(player_breakdown, stats_to_update):
    for player, points in stats_to_update.items():
        try:
            player_breakdown[player]
        except KeyError:
            player_breakdown[player] = 0
        player_breakdown[player] += points


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


def set_start_period_players(on_court_players, game_lineup, game_id, period):
    # All players start off the court
    for team in on_court_players:
        on_court_players[team] = []

    period_starting_lineup = game_lineup.loc[
        (game_lineup['Game_id'] == game_id) & (game_lineup['Period'] == period)
        ]
    for _, player in period_starting_lineup.iterrows():
        try:
            on_court_players[player['Team_id']].append(player['Person_id'])
        except KeyError:
            on_court_players[player['Team_id']] = [player['Person_id']]


def replace_players(on_court_players, leaving, incoming):
    # The team_id in the event of a substitution does not refer to the team of the substituted player
    for team_id in on_court_players:
        team = on_court_players[team_id]

        if leaving in team:
            team.remove(leaving)
            team.append(incoming)
            break


def reset_delayed_substitutions():
    """Sets default format for delayed_subs"""
    return {'leaving': [], 'incoming': []}


generate_data()
