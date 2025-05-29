import pandas as pd

data = None

def load_data(df):
    global data
    data = df

def query_data(query):
    global data
    if data is None:
        return "Сначала загрузите PDF файл."

    query_lower = query.lower()

    for _, row in data.iterrows():
        if (query_lower in row["Номер отправления"]) or            (query_lower in row["Артикул"]) or            (query_lower in row["Этикетка"]) or            (query_lower in row["Товар"].lower()):
            return f"""📦 *Найдено совпадение:*
*Товар:* {row['Товар']}
*Номер отправления:* {row['Номер отправления']}
*Артикул:* {row['Артикул']}
*Этикетка:* {row['Этикетка']}
*Кол-во:* {row['Кол-во']}
"""
    return "Ничего не найдено по запросу."
