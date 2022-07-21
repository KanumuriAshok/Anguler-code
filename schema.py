import psycopg2

user = "globals"
password = "globals"
host = "localhost"
port = 5432
database = "globals"


def create_schema(schema):
    connection = psycopg2.connect(
        database=database, user=user, password=password, host=host, port=port
    )
    # cursor = connection.cursor()
    CREATE_SCHEMA = f"CREATE SCHEMA IF NOT EXISTS {schema} AUTHORIZATION {user};"
    CREATE_TABLE1 = f"CREATE TABLE IF NOT EXISTS {schema}.data_output (username text)"
    CREATE_TABLE2 = f"CREATE TABLE IF NOT EXISTS {schema}.datainput (username text)"

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_SCHEMA)
            cursor.execute(CREATE_TABLE1)
            cursor.execute(CREATE_TABLE2)
