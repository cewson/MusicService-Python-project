# Импортирование библиотек 
import pandas as pd # Для работы с данными в формате таблиц 
from defs import load_data, save_data 

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
    save_data(dfs[table_name], table_name)



