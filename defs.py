# Импортирование библиотек 
import pandas as pd # Для работы с данными в формате таблиц 
import sqlite3 # Для работы с базой данных(БД)
import os.path # Для работы с файлами


# Загрудка данных из БД
def load_data(db_link:str, table_name:str):
    """
    Извлечение информации из базы данных
    
    :param db_link: Ссылка на базу данных
    :param table_name: Название таблицы в базе данных

    """
    # Проверка на существование БД
    if not os.path.exists(db_link):
        print(f"Ошибка: файл базы данных не найден — {db_link}")
    
    # Проверка: если таблицы не существует - выводим предупреждение
    try:
        with sqlite3.connect(db_link) as conn:
            sql_query = f"SELECT * FROM {table_name}"
            df_data = pd.read_sql(sql_query, conn)
            return df_data
        
    except Exception as e:
        print(f"Ошибка при загрузке таблицы '{table_name}'")
        return None


# Запись данных в файлы	
def save_data(df:pd.DataFrame, folder:str, file_name:str):
    """
    Сохранение данных в файлы
    
    :param df: Сохраняемая таблица
    :param folder: Папка для сохранения
    :param file_name: Название файла
    """

    if not isinstance(df, pd.DataFrame): 
        print('Ошибка: ожидался DataFrame') 
        return 
    
    if not os.path.exists(folder): 
        print(f'Ошибка: папка не найдена — {folder}') 
        return
    file_path = f'{folder}/{file_name}.xlsx'

    # Проверка: если файл существует - удаляем
    if os.path.exists(file_path):
        os.remove(file_path)

    # Сохранение
    df.to_excel(file_path, index=False)


# Поиск средней длительности треков 
def avr_duration(tracks:pd.DataFrame, genres:pd.DataFrame):
    """
    Функция поиска средней длительности треков по жанрам
    
    :param tracks: Таблица треков
    :param genres: Таблица жанров
    """
    
    tracks_in_genre = tracks.merge(genres, on='GenreId') # Объединение табли треки-жанры
    mean_duration = (tracks_in_genre
                     .groupby(genres['Name'])['Milliseconds']
                     .mean()
                     .reset_index()) # Подсчет и выбор необходимой информации
    
    return mean_duration


# Объединение таблиц и выбор необходимой информации
def combining_tables(tracks:pd.DataFrame, albums:pd.DataFrame, artists:pd.DataFrame):
    """
    Функция объеденения таблиц и выбора необходимой информации
    
    :param tracks: Таблица треков
    :param albums: Таблица альбомов
    :param artists: Таблица артистов
    """

    tracks_albums = tracks.merge(albums, on='AlbumId') # Объединение табли треки-альбомы
    all_info_track = tracks_albums.merge(artists, on='ArtistId') # Объединение таблиц треки-альбомы-исполнители
    results_table = (all_info_track[['Name_x', 'Title', 'Name_y']]
                     .rename(columns={'Name_x': 'SongName', 'Name_y': 'ArtistName'}) ) #Выбор необходимой информации
    
    return results_table


# Оопределение топ-5 прибыльных жанров на основе суммы продаж 
def profitable_genres(genres:pd.DataFrame, tracks:pd.DataFrame, invoice_items:pd.DataFrame):
    """
    Функция поиска топ-5 прибыльных жанров на основе суммы продаж
    
    :param genres: Таблица жанров
    :param tracks: Таблица треков
    :param invoice_items: Таблица продаж треков
    """

    invoice_track = invoice_items.merge(tracks, on='TrackId') # Объединение таблиц треки-продажи треков
    invoice_track_genre = invoice_track.merge(genres, on='GenreId') # # Объединение таблиц треки-продажи треков-жанры треков
    groupby_genre = (invoice_track_genre
                     .groupby(['GenreId', 'Name_y'])['UnitPrice_x']
                     .sum()
                     .reset_index()
                     .sort_values('UnitPrice_x', ascending=False)
                     .head(5)) # Подсчет и выбор необходимой информации
    
    return groupby_genre


# Писк топ клиентов по покупке в жанре 
def purchases_in_genre(genres:pd.DataFrame, 
                       search_genre:str, 
                       tracks:pd.DataFrame, 
                       invoice_items:pd.DataFrame, 
                       invoices:pd.DataFrame, 
                       customers:pd.DataFrame):
    """
    Функция поиска топ клиентов по покупке в жанре
    
    :param genres: Таблица жанров
    :param search_genre: Жанр для поиска
    :param tracks: Таблица треков
    :param invoice_items: Таблица продаж треков
    :param invoices: Таблица продаж
    :param customers: Таблица клинтов
    """
    
    genre_row = genres.loc[genres['Name'] == search_genre, 'GenreId']
 
    # Проверка: если введен неверный жанр - вывести предупреждение, остановить функцию
    if genre_row.empty: 
        print('Ошибка: неверный жанр') 
        return None
    
    genre_id = genre_row.iloc[0]

    genre_tracks = tracks.loc[tracks['GenreId'] == genre_id, 'TrackId'] # Выбор треков по определенному жанру
    genre_items = invoice_items.merge(genre_tracks, on='TrackId') # Объединение треки жанра-продажи треков
    genre_invoice = invoices.merge(genre_items, on='InvoiceId') # ОБъединение с треки жанра-продажи треков-продажи
    customersid = (genre_invoice
                   .groupby('CustomerId')
                   .size()
                   .reset_index(name='TrackCount')) # Подсчет и выбор нужной информации
    customers_info = (customers.merge(customersid, on='CustomerId')
                      .sort_values('TrackCount', ascending=False)) # Объединение с таблицой клиентов
    return customers_info
