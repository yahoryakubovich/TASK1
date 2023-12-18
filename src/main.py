from data_readers.json_data_reader import JsonDataReader
from database.database_connector import DatabaseConnector
from database.database_manager import DatabaseManager
from data_exporters.data_exporter_for_rooms import DataExporterForRooms
from data_exporters.data_exporter_for_students import DataExporterForStudents
from config import *

if __name__ == "__main__":
    rooms_file_path = '/home/yahoryakubovich/Desktop/TASK1/rooms.json'
    students_file_path = '/home/yahoryakubovich/Desktop/TASK1/students.json'

    db_connector = DatabaseConnector(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
    db_connector.connect()

    database_manager = DatabaseManager(db_connector.connection)

    database_manager.create_rooms_table()
    database_manager.create_students_table()

    rooms_data = JsonDataReader.read(rooms_file_path)
    students_data = JsonDataReader.read(students_file_path)

    # database_manager.insert_rooms_data(rooms_data)
    # database_manager.insert_students_data(students_data)

    data_exporter = DataExporterForRooms(db_connector.connection)

    data_exporter.export_to_format('rooms', 'exported_data_rooms.json', 'json')

    data_exporter.export_to_format('rooms', 'exported_data_rooms.xml', 'xml')

    data_exporter = DataExporterForStudents(db_connector.connection)

    data_exporter.export_to_format('students', 'exported_data_students.json', 'json')

    data_exporter.export_to_format('students', 'exported_data_students.xml', 'xml')

    db_connector.close()
