import pandas as pd

def setup_dataframe(data):
    """
    :param data: raw text file data
    :return: dataframe with first line of data as columns
    """
    data_list = data.split('\n')
    columns = data_list.pop(0).split('\t')

    for index in range(len(data_list)):
        data_list[index] = data_list[index].split('\t')
    return pd.DataFrame(data_list, columns=columns)

def convert_txt_to_df(FILE_PATH):
    file_data = open(FILE_PATH, 'r').read()
    return setup_dataframe(file_data)
