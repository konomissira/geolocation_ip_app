import os
import psycopg2

# Use environment variables provided via Docker Compose
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def connect_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            connect_timeout=5
        )
        print("Connected to DB via TCP")
        return conn
    except Exception as e:
        print(f"Failed to connect to DB: {e}")
        return None

def create_table(conn):
    create_query = """
    CREATE TABLE IF NOT EXISTS ip_geolocation (
        id SERIAL PRIMARY KEY,
        ip VARCHAR(45),
        city TEXT,
        region TEXT,
        country TEXT,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION
    );
    """
    with conn.cursor() as cur:
        cur.execute(create_query)
        conn.commit()

def insert_data(conn, data):
    insert_query = """
    INSERT INTO ip_geolocation (ip, city, region, country, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    with conn.cursor() as cur:
        for row in data:
            cur.execute(insert_query, (
                row["ip"],
                row["city"],
                row["region"],
                row["country"],
                row["latitude"],
                row["longitude"]
            ))
        conn.commit()

if __name__ == "__main__":
    sample_data = [
        {
            "ip": "8.8.8.8",
            "city": "Mountain View",
            "region": "California",
            "country": "United States",
            "latitude": 37.388,
            "longitude": -122.074
        }
    ]

    conn = connect_db()
    if conn:
        create_table(conn)
        insert_data(conn, sample_data)
        print("Data inserted successfully.")
        conn.close()
