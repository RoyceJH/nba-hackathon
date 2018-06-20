import pandas as pd


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
    file_data = open(FILE_PATH, 'r').read()
    return setup_dataframe(file_data)


def convert_cols_to_int(df, columns):
    """
    :param df: Dataframe to modify
    :param columns: List of columns to convert to int
    :return: Modified df
    """
    for column in columns:
        df[column] = df[column].astype(int)