import sqlite3


def check_db():

	sqlite_create_table_query = ''' CREATE TABLE if not exists Channels (
									name  TEXT,
									channel_id TEXT	NOT NULL UNIQUE PRIMARY KEY,
									status BOOL); '''

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

def get_actual_channels():

	sqlite_select_query = ''' SELECT channel_id FROM Channels	
							  WHERE status = True; '''

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

def get_dead_channels():

	sqlite_select_query = ''' SELECT channel_id FROM Channels	
							  WHERE status = False; '''

	pure_data =[]

	try:
		sqlite_connection = sqlite3.connect('user_bot.db')
		print("Подключен к базе user_bot.db для получения мёртвых каналов")
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

def add_data_to_channels(channel, status):

	sqlite_insert_query = ''' INSERT INTO Channels
							  (channel_id, status)
							  Values
							  (?, ?) '''

	try:
		sqlite_connection = sqlite3.connect('user_bot.db')
		cursor = sqlite_connection.cursor()
		records_to_insert = (channel, status)
		cursor.execute(sqlite_insert_query, records_to_insert)
		sqlite_connection.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite, не получилось добавить данные", error)

	finally:
		if sqlite_connection:
			sqlite_connection.close()