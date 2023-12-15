import json
import psycopg2


def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {file_path}")
    return None


def write_to_postgres(data_list, connection_params):
    try:
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()
        for data in data_list:
            id_as_int = int(data['id'])

            cursor.execute("""
                INSERT INTO rooms (id, name)
                VALUES (%s, %s)
            """, (id_as_int, data['name']))

        connection.commit()
        print("Data successfully written to PostgreSQL!")

    except psycopg2.Error as e:
        print(f"Error writing to PostgreSQL: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()


# Замените 'example.json' на путь к вашему JSON файлу
json_data = read_json('rooms.json')

if json_data:
    # Замените параметры подключения на свои
    connection_params = {
        'host': 'localhost',
        'database': 'dormitory',
        'user': 'postgres',
        'password': '12345678',
        'port': '5432',
    }

    write_to_postgres(json_data, connection_params)
