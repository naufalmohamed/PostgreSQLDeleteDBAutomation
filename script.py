import psycopg2
from psycopg2 import sql

# Database connection parameters
host = "localhost"  # Hostname of your PostgreSQL server
port = "5432"       # Port number your PostgreSQL server is listening on
user = "postgres"   # Username to connect to the PostgreSQL server
password = "your_password"  # Password for the PostgreSQL user

# Databases to keep (specify the names you want to keep in this list)
databases_to_keep = ["mydb1", "mydb2", "mydb3"]

try:
    # Connect to PostgreSQL
    connection = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
    )
    
    # Enable autocommit mode
    connection.autocommit = True

    # Create a cursor object
    cursor = connection.cursor()

    # Execute a query to fetch all database names
    cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")

    # Fetch all results
    databases = cursor.fetchall()

    # Delete databases not in the list of databases to keep
    for db in databases:
        db_name = db[0]
        if db_name not in databases_to_keep:
            try:
                # Use SQL identifiers to properly quote database names
                cursor.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(db_name)))
                print(f"Deleted database: {db_name}")
            except Exception as e:
                print(f"Error deleting database {db_name}: {e}")

except Exception as error:
    print(f"Error: {error}")

finally:
    if 'connection' in locals():
        cursor.close()
        connection.close()
