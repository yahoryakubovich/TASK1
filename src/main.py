from data_readers.json_data_reader import JsonDataReader
from database.database_connector import DatabaseConnector
from database.database_manager import DatabaseManager

DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'dormitory'
DB_USER = 'postgres'
DB_PASSWORD = '831212'

# if __name__ == "__main__":
#     rooms_file_path = '/home/yahoryakubovich/Desktop/TASK1/rooms.json'
#     students_file_path = '/home/yahoryakubovich/Desktop/TASK1/students.json'
#
#     db_connector = DatabaseConnector(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
#     db_connector.connect()
#
#     database_manager = DatabaseManager(db_connector.connection)
#
#     database_manager.create_rooms_table()
#     database_manager.create_students_table()
#
#     rooms_data = JsonDataReader.read(rooms_file_path)
#     students_data = JsonDataReader.read(students_file_path)
#
#     # database_manager.insert_rooms_data(rooms_data)
#     # database_manager.insert_students_data(students_data)
#
#     data_exporter = DataExporterForRooms(db_connector.connection)
#
#     data_exporter.export_to_format('rooms', 'exported_data_rooms.json', 'json')
#
#     data_exporter.export_to_format('rooms', 'exported_data_rooms.xml', 'xml')
#
#     data_exporter = DataExporterForStudents(db_connector.connection)
#
#     data_exporter.export_to_format('students', 'exported_data_students.json', 'json')
#
#     data_exporter.export_to_format('students', 'exported_data_students.xml', 'xml')
#
#     db_connector.close()

import argparse
from pathlib import Path
from data_readers.json_data_reader import JsonDataReader
from database.database_connector import DatabaseConnector
from database.database_manager import DatabaseManager
from data_exporters.data_exporter_json import DataExporterJson
from data_exporters.data_exporter_xml import DataExporterXml


def process_data(students_file_path, rooms_file_path, output_format):
    db_connector = DatabaseConnector(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
    db_connector.connect()

    database_manager = DatabaseManager(db_connector.connection)

    database_manager.create_rooms_table()
    database_manager.create_students_table()

    rooms_data = JsonDataReader.read(rooms_file_path)
    students_data = JsonDataReader.read(students_file_path)

    if output_format == 'json':
        data_exporter_rooms = DataExporterJson(db_connector.connection)
        data_exporter_students = DataExporterJson(db_connector.connection)
        data_exporter_rooms.export_rooms_to_json('rooms', f'exported_data_rooms.{output_format}')
        data_exporter_students.export_rooms_to_json('students', f'exported_data_students.{output_format}')
    elif output_format == 'xml':
        data_exporter_rooms = DataExporterXml(db_connector.connection)
        data_exporter_students = DataExporterXml(db_connector.connection)
        data_exporter_rooms.export_rooms_to_xml('rooms', f'exported_data_rooms.{output_format}')
        data_exporter_students.export_rooms_to_xml('students', f'exported_data_students.{output_format}')
    else:
        raise ValueError("Invalid output format. Supported formats: 'json' or 'xml'.")

    db_connector.close()


if __name__ == "__main__":
    # Определение аргументов командной строки
    parser = argparse.ArgumentParser(description='Process students and rooms data.')
    parser.add_argument('students', type=Path, help='Path to the students file')
    parser.add_argument('rooms', type=Path, help='Path to the rooms file')
    parser.add_argument('format', choices=['json', 'xml'], help='Output format (json or xml)')

    # Получение значений аргументов
    args = parser.parse_args()

    students_file_path = args.students
    rooms_file_path = args.rooms
    output_format = args.format

    process_data(students_file_path, rooms_file_path, output_format)
