import json
import psycopg2
from psycopg2 import sql

# Замените на свои данные для подключения к базе данных
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'dormitory'
DB_USER = 'postgres'
DB_PASSWORD = '12345678'

# Функция для чтения данных из JSON файла
class JsonDataReader:
    @staticmethod
    def read(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

# Функция для подключения к базе данных
class DatabaseConnector:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def close(self):
        if self.connection:
            self.connection.close()

# Функция для создания таблицы Rooms
class DatabaseManager:
    def __init__(self, connection):
        self.connection = connection

    def create_rooms_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                );
            """)
        self.connection.commit()

    def create_students_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    birthday DATE NOT NULL,
                    sex CHAR(1) NOT NULL,
                    room_id INT REFERENCES rooms(id)
                );
            """)
        self.connection.commit()

    def insert_rooms_data(self, rooms_data):
        with self.connection.cursor() as cursor:
            for room in rooms_data:
                cursor.execute(sql.SQL("""
                    INSERT INTO rooms (id, name)
                    VALUES (%s, %s);
                """), (room['id'], room['name']))
        self.connection.commit()

    def insert_students_data(self, students_data):
        with self.connection.cursor() as cursor:
            for student in students_data:
                cursor.execute(sql.SQL("""
                    INSERT INTO students (id, name, birthday, sex, room_id)
                    VALUES (%s, %s, %s, %s, %s);
                """), (student['id'], student['name'], student['birthday'], student['sex'], student['room']))
        self.connection.commit()

if __name__ == "__main__":
    rooms_file_path = 'rooms.json'
    students_file_path = 'students.json'

    # Подключение к базе данных
    db_connector = DatabaseConnector(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
    db_connector.connect()

    # Создание объекта класса DatabaseManager
    database_manager = DatabaseManager(db_connector.connection)

    # Создание таблиц
    database_manager.create_rooms_table()
    database_manager.create_students_table()

    # Чтение данных из JSON файлов
    rooms_data = JsonDataReader.read(rooms_file_path)
    students_data = JsonDataReader.read(students_file_path)

    # Вставка данных в таблицы
    database_manager.insert_rooms_data(rooms_data)
    database_manager.insert_students_data(students_data)

    # Закрытие подключения
    db_connector.close()
