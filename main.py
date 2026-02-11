# Импортирование библиотек 
import pandas as pd # Для работы с данными в формате таблиц 
from defs import load_data, save_data, avr_duration, combining_tables, purchases_in_genre,  profitable_genres

# Список названий таблиц из базы данных
tables = [
    'albums',
    'artists', 
    'customers', 
    'employees',
    'genres', 
    'invoices', 
    'invoice_items', 
    'media_types',
    'playlists', 
    'playlist_track', 
    'tracks'    
]

# Вагрузка данных из базы данных
dfs = {name: load_data('chinook.db', name) for name in tables}

# Сохранение данных в локальное хранилище
for table_name, table_data in dfs.items():
    save_data(dfs[table_name], 'data', table_name)

# Поиск средней длительности трека жанрах и сохранение результата
df_avr_duration = avr_duration(dfs['tracks'], dfs['genres'])
save_data(df_avr_duration, 'results', 'avr_duration')

# Объединение таблиц tracks, albums и artists и сохранение результата
df_combining_tables = combining_tables(dfs['tracks'], dfs['albums'], dfs['artists'])
save_data(df_combining_tables, 'results', 'tracks_album_artist')

# Определение топ-5 самых прибыльных жанров  на основе суммы продаж и сохранение результата 
top_5_genres = profitable_genres(dfs['genres'], dfs['tracks'], dfs['invoice_items'])
save_data(top_5_genres, 'results', 'top_5_genres')

# Поиск клиентов, которые купили больше всего треков в жанре "Rock" и сохранение результата
top_genre_customers = purchases_in_genre(dfs['genres'], 'Rock', dfs['tracks'], dfs['invoice_items'], dfs['invoices'], dfs['customers'])
save_data(top_genre_customers, 'results', 'top_genre_customers')

