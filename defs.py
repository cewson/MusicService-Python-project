import pandas as pd
import sqlite3
print("defs.py подключен!")

# class UnsupportedTableName(Exception): 
#     """
#     Ошибка: неподдерживаемая операция
#     """
#     def __str__(self):
#         return "Ошибка: неподдерживаемая операция"
    
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
def save_data(df, folder, file_name):
    df.to_excel(f'{folder}/{file_name}.xlsx', index=False)


# поиск средней длительности треков avr_duration
def avr_duration(tracks, genres):

    merged = tracks.merge(genres, on='GenreId')
    merged_mean = merged.groupby(genres['Name'])['Milliseconds'].mean().reset_index()
    
    return merged_mean

# объединение таблиц  combining_tables и выбор необходимой информации

def combining_tables(tracks, albums, artists):

    merge1 = tracks.merge(albums, on='AlbumId')
    merge2 = merge1.merge(artists, on='ArtistId')
    results_table = merge2[['Name_x', 'Title', 'Name_y']].rename(columns={'Name_x': 'SongName', 'Name_y': 'ArtistName'}) 
    return results_table


# топ клиентов, по покупке в жанре   purchases_in_genre
def purchases_in_genre(genres, search_genre, tracks, invoice_items, invoices, customers):
   
    genre_row = genres.loc[genres['Name'] == search_genre, 'GenreId']
    
    if genre_row.empty: 
        return pd.DataFrame() # жанр не найден
    genre_id = genre_row.iloc[0]

    rock_tracks = tracks.loc[tracks['GenreId'] == genre_id, 'TrackId']
    rock_items = invoice_items.merge(rock_tracks, on='TrackId')
    rock_invoice = invoices.merge(rock_items, on='InvoiceId')
    customersid = rock_invoice.groupby('CustomerId').size().reset_index(name='TrackCount')
    customers_info = customers.merge(customersid, on='CustomerId').sort_values('TrackCount', ascending=False)
    return customers_info
