import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from psycopg2 import sql


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
