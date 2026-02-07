import pandas as pd
import sqlite3
print("defs.py подключен!")

class UnsupportedTableName(Exception): 
    """
    Ошибка: неподдерживаемая операция
    """
    def __str__(self):
        return "Ошибка: неподдерживаемая операция"
    
# загрузка данных	load_data
def load_data(db_link:str, table_name:str):
    """
    Извлечение информации из базы данных
    
    :param db_link: Ссылка на базу данных
    :param table_name: Название таблицы в базе данных

    """

    with sqlite3.connect(db_link) as conn:
        sql_query = f'SELECT * FROM {table_name}'
        df_data = pd.read_sql(sql_query, conn)
    
    return df_data

# запись данных в файлы	save_data
def save_data(df, file_name):
    df.to_excel(f'data/{file_name}.xlsx', index=False)



