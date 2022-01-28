import sqlite3


def check_db():

	sqlite_create_table_query = ''' CREATE TABLE if not exists Channels (
									channel_id TEXT NULL UNIQUE PRIMARY KEY,
									name  TEXT NOT NULL,
									channel_link TEXT	NOT NULL,
									channel_access_hash TEXT NULL UNIQUE,
									status BOOL,
									messaging BOOL); '''

	try:
		sqlite_connection = sqlite3.connect('user_bot.db')
		cursor = sqlite_connection.cursor()
		cursor.execute(sqlite_create_table_query)
		sqlite_connection.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite", error)

	finally:
		if (sqlite_connection):
			sqlite_connection.close
			print("Соединение с базой user_bot.db прошло успешно")

def get_actual_data(status, messaging ):

	sqlite_select_query = ''' SELECT channel_link FROM Channels	
							  WHERE status = ? AND messaging = ?; '''

	pure_data =[]								

	try:
		sqlite_connection = sqlite3.connect('user_bot.db')
		print("Подключен к базе user_bot.db для получения актуальных каналов")
		cursor = sqlite_connection.cursor()
		data_to_filter = (status, messaging)
		cursor.execute(sqlite_select_query, data_to_filter)
		records = cursor.fetchall()
		cursor.close()
		for sloi1 in records:
			for sloi2 in sloi1:
				pure_data.append(sloi2)

	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite", error)

	finally:
		if sqlite_connection:
			sqlite_connection.close()
			print("Соединение с user_bot.db прошло успешно, данные получены!")

	return pure_data

def add_data_to_channels(channel_id,name, channel_link, status, channel_access_hash, messaging):

	sqlite_insert_query = ''' INSERT INTO Channels
							  (channel_id, name, channel_link, status, channel_access_hash, messaging)
							  Values
							  (?, ?, ?, ?, ?, ?) '''

	try:
		sqlite_connection = sqlite3.connect('user_bot.db')
		cursor = sqlite_connection.cursor()
		records_to_insert = (channel_id, name, channel_link, status, channel_access_hash, messaging)
		cursor.execute(sqlite_insert_query, records_to_insert)
		sqlite_connection.commit()
		cursor.close()
		print("Данные успешно записаны в user_bot.db")

	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite, не получилось добавить данные", error)

	finally:
		if sqlite_connection:
			sqlite_connection.close()

def get_data_to_parsing():

	sqlite_select_query = ''' SELECT channel_link FROM Channels	
							  WHERE status = TRUE; '''

	pure_data =[]								

	try:
		sqlite_connection = sqlite3.connect('user_bot.db')
		print("Подключен к базе user_bot.db для получения актуальных каналов")
		cursor = sqlite_connection.cursor()
		cursor.execute(sqlite_select_query)
		records = cursor.fetchall()
		cursor.close()
		for sloi1 in records:
			for sloi2 in sloi1:
				pure_data.append(sloi2)

	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite", error)

	finally:
		if sqlite_connection:
			sqlite_connection.close()
			print("Соединение с user_bot.db прошло успешно, данные получены!")

	return pure_data


def update_sqlite_table():
	pass