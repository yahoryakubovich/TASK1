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
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Функция для подключения к базе данных
def connect_to_database():
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connection

# Функция для создания таблицы Rooms
def create_rooms_table(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
        """)
    connection.commit()

# Функция для создания таблицы Students
def create_students_table(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                birthday DATE NOT NULL,
                sex CHAR(1) NOT NULL,
                room_id INT REFERENCES rooms(id)
            );
        """)
    connection.commit()

# Функция для вставки данных в таблицу Rooms
def insert_rooms_data(connection, rooms_data):
    with connection.cursor() as cursor:
        for room in rooms_data:
            cursor.execute(sql.SQL("""
                INSERT INTO rooms (id, name)
                VALUES (%s, %s);
            """), (room['id'], room['name']))
    connection.commit()

# Функция для вставки данных в таблицу Students
def insert_students_data(connection, students_data):
    with connection.cursor() as cursor:
        for student in students_data:
            cursor.execute(sql.SQL("""
                INSERT INTO students (id, name, birthday, sex, room_id)
                VALUES (%s, %s, %s, %s, %s);
            """), (student['id'], student['name'], student['birthday'], student['sex'], student['room']))
    connection.commit()

if __name__ == "__main__":
    rooms_file_path = 'rooms.json'
    students_file_path = 'students.json'

    # Чтение данных из JSON файлов
    rooms_data = read_json(rooms_file_path)
    students_data = read_json(students_file_path)

    # Подключение к базе данных
    connection = connect_to_database()

    # Создание таблиц
    create_rooms_table(connection)
    create_students_table(connection)

    # Вставка данных в таблицы
    insert_rooms_data(connection, rooms_data)
    insert_students_data(connection, students_data)

    # Закрытие подключения
    connection.close()
