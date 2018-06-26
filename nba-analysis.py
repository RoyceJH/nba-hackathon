import re

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
    delayed_subs = {'leaving': [], 'incoming': []}

    # get_start_period_players(on_court_players, game_lineup, game['Game_id'][0], 1)

    for _, play in game.iterrows():
        _, _, event_description, action_description = lookup_event(event_code, play)

        if 'Start Period' in event_description:
            set_start_period_players(on_court_players, game_lineup, game_id, play['Period'])
        elif 'Made Shot' in event_description or 'Technical' in action_description:
            points = play['Option1']
            scoring_team = play['Team_id']
            stats_to_update = calculate_stats_to_update(on_court_players, points, scoring_team)
            update_stats(player_breakdown, stats_to_update)
        elif 'Substitution' in event_description:
            if halt_player_change:
                delayed_subs['leaving'].append(play['Person1'])
                delayed_subs['incoming'].append(play['Person2'])
            else:
                leaving_player = play['Person1']
                incoming_player = play['Person2']
                replace_players(on_court_players, leaving_player, incoming_player)
        elif 'Free Throw' in event_description and 'Technical' not in action_description:
            shot_number, total_shot = extract_free_throw_shots(action_description)
            points = play['Option1']
            scoring_team = play['Team_id']
            stats_to_update = calculate_stats_to_update(on_court_players, points, scoring_team)
            update_stats(player_breakdown, stats_to_update)

            if shot_number < total_shot:
                # Want to set true to delay substitutions when free throws are not done
                halt_player_change = True
            elif shot_number == total_shot:
                # Want to confirm that free throws are done and substitutions can now be made
                halt_player_change = False

                # Should be the same number of incoming and outgoing players and indexed by the same team
                for idx in range(len(delayed_subs['leaving'])):
                    replace_players(on_court_players, delayed_subs['leaving'][idx], delayed_subs['incoming'][idx])

                delayed_subs = reset_delayed_substitutions()
        elif 'Technical' in action_description:
            print('hi')
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


def lookup_event(event_code, play):
    event = event_code.loc[
        (event_code['"Event_Msg_Type"'] == play['Event_Msg_Type']) & (event_code['"Action_Type"'] == play['Action_Type'])
    ]
    return event.values.flatten()


def replace_players(on_court_players, leaving, incoming):
    # The team_id in the event of a substitution does not refer to the team of the substituted player
    for team_id in on_court_players:
        team = on_court_players[team_id]

        if leaving in team:
            team.remove(leaving)
            team.append(incoming)
            break


def extract_free_throw_shots(description):
    """
    Extract the shot number and total shots of free throws
    :param description: Ie: `Free Throw 1 of 2`
    :return: 1, 2
    """

    try:
        a, b = description.strip('"').strip().split('Free Throw ')[1].split(' of ')
    except:
        print('hi')
    return description.strip('"').strip().split('Free Throw ')[1].split(' of ')


def reset_delayed_substitutions():
    """Sets default format for delayed_subs"""
    return {'leaving': [], 'incoming': []}



generate_data()
