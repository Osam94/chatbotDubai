import pandas as pd
user_data = {}
def save_user_data(user_id, df): user_data[user_id] = df
def query_user_data(user_id, query):
    df = user_data.get(user_id)
    if df is None:
        return "⚠️ Сначала отправьте PDF-файл."
    query = query.lower()
    for _, row in df.iterrows():
        if (query in row["Номер отправления"]) or            (query in row["Артикул"]) or            (query in row["Этикетка"]) or            (query in row["Товар"].lower()):
            return f"""📦 *Найдено совпадение:*
*Товар:* {row['Товар']}
*Номер отправления:* {row['Номер отправления']}
*Артикул:* {row['Артикул']}
*Этикетка:* {row['Этикетка']}
*Кол-во:* {row['Кол-во']}
"""
    return "❌ Ничего не найдено по запросу."
