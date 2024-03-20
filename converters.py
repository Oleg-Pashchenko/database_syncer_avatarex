import numpy as np
import requests
import pandas as pd


def download_sheet(link: str):
    file_id = link.replace('https://docs.google.com/spreadsheets/d/', '').split('/')[0]
    file_path = f'result.xlsx'
    try:
        url = f'https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx'
        response = requests.get(url)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return file_path

    except Exception as e:
        return None


def get_knowledge_data(link: str):
    filename = download_sheet(link)
    data = {}
    df = pd.read_excel(filename)
    list_of_arrays = list(df.iloc)

    for i in list_of_arrays:
        data[i[0]] = i[1]
    return data


def get_database_data(link: str):
    filename = download_sheet(link)
    try:
        df = pd.read_excel(filename, engine='openpyxl')
    except Exception as e:
        df = pd.read_excel(filename, engine='xlrd')

    list_of_dicts = [dict(zip(df.columns, [item.item() if isinstance(item, np.generic) else item for item in row]))
                     for row in df.values]
    return list_of_dicts
