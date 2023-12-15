import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import psycopg2
from psycopg2 import sql
from config import *


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


class DataExporterForRooms:
    def __init__(self, connection):
        self.connection = connection

    def export_to_format(self, table_name, file_path, export_format):
        with self.connection.cursor() as cursor:
            cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
            data = cursor.fetchall()

        if export_format == 'json':
            self._export_to_json(file_path, data)
        elif export_format == 'xml':
            self._export_to_xml(file_path, data)
        else:
            raise ValueError("Invalid export format. Supported formats: 'json' or 'xml'.")

    def _export_to_json(self, file_path, data):
        formatted_data = [{"id": row[0], "name": row[1]} for row in data]
        with open(file_path, 'w') as file:
            json.dump(formatted_data, file, indent=2)

    def _export_to_xml(self, file_path, data):
        root = ET.Element("data")
        for item in data:
            element = ET.SubElement(root, "item")
            for i, column_name in enumerate(('id', 'name')):
                sub_element = ET.SubElement(element, column_name)
                sub_element.text = str(item[i])

        xml_data = ET.tostring(root, encoding='utf-8', method='xml')
        parsed_xml = minidom.parseString(xml_data)
        pretty_xml = parsed_xml.toprettyxml(indent="  ")

        with open(file_path, 'w') as file:
            file.write(pretty_xml)

class DataExporterForStudents:
    def __init__(self, connection):
        self.connection = connection

    def export_to_format(self, table_name, file_path, export_format):
        with self.connection.cursor() as cursor:
            cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
            data = cursor.fetchall()

        if export_format == 'json':
            self._export_to_json(file_path, data)
        elif export_format == 'xml':
            self._export_to_xml(file_path, data)
        else:
            raise ValueError("Invalid export format. Supported formats: 'json' or 'xml'.")

    def _export_to_json(self, file_path, data):
        formatted_data = []
        for row in data:
            formatted_row = {
                "id": row[0],
                "name": row[1],
                "birthday": str(row[2]),
                "sex": row[3],
                "room": row[4]
            }
            formatted_data.append(formatted_row)

        with open(file_path, 'w') as file:
            json.dump(formatted_data, file, indent=2)

    def _export_to_xml(self, file_path, data):
        root = ET.Element("data")
        for row in data:
            element = ET.SubElement(root, "item")
            for i, column_name in enumerate(('id', 'name', 'birthday', 'sex', 'room')):
                sub_element = ET.SubElement(element, column_name)
                sub_element.text = str(row[i])

        xml_data = ET.tostring(root, encoding='utf-8', method='xml')
        parsed_xml = minidom.parseString(xml_data)
        pretty_xml = parsed_xml.toprettyxml(indent="  ")

        with open(file_path, 'w') as file:
            file.write(pretty_xml)


if __name__ == "__main__":
    rooms_file_path = 'rooms.json'
    students_file_path = 'students.json'

    # Подключение к базе данных
    db_connector = DatabaseConnector(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
    db_connector.connect()

    # # Создание объекта класса DatabaseManager
    # database_manager = DatabaseManager(db_connector.connection)
    #
    # # Создание таблиц
    # database_manager.create_rooms_table()
    # database_manager.create_students_table()

    # # Чтение данных из JSON файлов
    # rooms_data = JsonDataReader.read(rooms_file_path)
    # students_data = JsonDataReader.read(students_file_path)

    # # Вставка данных в таблицы
    # database_manager.insert_rooms_data(rooms_data)
    # database_manager.insert_students_data(students_data)

    data_exporter = DataExporterForRooms(db_connector.connection)

    # Выгрузка данных в JSON
    data_exporter.export_to_format('rooms', 'exported_data_rooms.json', 'json')

    # Выгрузка данных в XML
    data_exporter.export_to_format('rooms', 'exported_data_rooms.xml', 'xml')

    data_exporter = DataExporterForStudents(db_connector.connection)

    # Выгрузка данных в JSON
    data_exporter.export_to_format('students', 'exported_data_students.json', 'json')

    # Выгрузка данных в XML
    data_exporter.export_to_format('students', 'exported_data_students.xml', 'xml')
    # Закрытие подключения
    db_connector.close()
