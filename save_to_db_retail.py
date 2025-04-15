from database_utils import DatabaseConnector

db = DatabaseConnector()

def save_detected_product(json_txt):
    conn = db.ini_db_engine()
    if conn is None:
        return
    try:
        cursor = conn.cursor()

        # Check if the table AITransactionCount exists
        cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'AITransactionCount'
        """)
        
        table_exists = cursor.fetchone()[0] == 1

        if not table_exists:
            print("Table 'AITransactionCount' not found. Creating table...")
            cursor.execute("""
            CREATE TABLE AITransactionCount (
                Till_area_count NVARCHAR(MAX) NOT NULL
            )
            """)
            print("Table 'AITransactionCount' created.")

            cursor.execute("""
            INSERT INTO AITransactionCount (Till_area_count) 
            VALUES ('[]')  -- Empty JSON array as a placeholder
            """)
            conn.commit()
        else:
            # Check if column 'Till_area_count' exists
            cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'AITransactionCount' AND COLUMN_NAME = 'Till_area_count'
            """)
            if cursor.fetchone() is None:
                print("Column 'Till_area_count' not found. Adding column...")
                cursor.execute("ALTER TABLE AITransactionCount ADD Till_area_count NVARCHAR(MAX)")
                conn.commit()

            
        # Proceed with the update query
        query = """
        UPDATE AITransactionCount
        SET Till_area_count = ?
        """
        cursor.execute(query, (json_txt,))
        conn.commit()

        conn.close()
        print(f"Item details saved to database.")
    except Exception as e:
        print("Error inserting data:", e)

