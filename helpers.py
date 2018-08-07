import pandas as pd
import xlsxwriter


def setup_dataframe(data):
    """
    :param data: Raw text file data
    :return: Dataframe with first line of data as columns
    """
    # Strip to remove last empty new line
    data_list = data.strip().split('\n')
    columns = data_list.pop(0).split('\t')

    for index in range(len(data_list)):
        data_list[index] = data_list[index].split('\t')
    return pd.DataFrame(data_list, columns=columns)


def convert_txt_to_df(FILE_PATH):
    print('Setting up df for : {}'.format(FILE_PATH))
    file_data = open(FILE_PATH, 'r').read()
    return setup_dataframe(file_data)


def convert_cols_to_int(df, columns):
    """
    :param df: Dataframe to modify
    :param columns: List of columns to convert to int
    :return: Modified df
    """
    for column in columns:
        column_to_update = ''
        if column in df:
            column_to_update = column
        # For event_code dataframe, the columns are formatted as nested strings
        elif '"{}"'.format(column) in df:
            column_to_update = '"{}"'.format(column)

        if column_to_update:
            df[column_to_update] = df[column_to_update].astype(int)


def create_workbook():
    return xlsxwriter.Workbook('coder_factory.xlsx')


def setup_worksheet(wb):
    ws = wb.add_worksheet()
    col_headers = ['Game_ID', 'Player_ID', 'Player_Plus/Minus']

    for i in range(len(col_headers)):
        ws.write(0, i, col_headers[i])

    return ws


def add_dict_to_worksheet(ws, game_data_dict, game_id, row):
    """
    :param ws: Worksheet to add data
    :param game_data_dict: Plus Minus data for one game
    :param game_id: game id
    :param row: current row to write to worksheet
    :return: row to write to next
    """
    for player_id in game_data_dict:
        plus_minus = game_data_dict[player_id]
        ws.write(row, 0, game_id)
        ws.write(row, 1, player_id)
        ws.write(row, 2, plus_minus)
        row += 1

    return row


def get_time_diff(start, end):
    ms = 0
    delta = end - start
    ms += delta.seconds * 1000
    ms += delta.microseconds / 1000
    return ms
