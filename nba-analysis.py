import pandas as pd

EVENT_PATH = './NBA Hackathon - Event Codes.txt'
GAME_LOG_PATH = './NBA Hackathon - Game Lineup Data Sample (50 Games).txt'
PLAY_DATA_PATH = './NBA Hackathon - Play by Play Data Sample (50 Games).txt'

event_data = open(EVENT_PATH, 'r').read()
game_log_data = open(GAME_LOG_PATH, 'r').read()
play_data = open(PLAY_DATA_PATH, 'r').read()

def setup_dataframe(data):
    data_split = data.split('\n')
    columns = data_split.pop(0).split('\t')

    for index in range(len(data_split)):
        data_split[index] = data_split[index].split('\t')
    return pd.DataFrame(data_split, columns=columns)

event_df = setup_dataframe(event_data)
print(event_data.split('\n'))

