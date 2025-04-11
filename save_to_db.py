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
        
        # If the table does not exist, create it
        if cursor.fetchone()[0] == 0:
            print("Table 'AITransactionCount' not found. Creating table...")
            cursor.execute("""
            CREATE TABLE AITransactionCount (
                
                count NVARCHAR(MAX) NOT NULL
            )
            """)
            print("Table 'AITransactionCount' created.")
            
            cursor.execute("""
            INSERT INTO AITransactionCount (count) 
            VALUES ('[]')  -- Empty JSON array as a placeholder
            """)
            conn.commit()
            
        # Proceed with the update query
        query = """
        UPDATE AITransactionCount
        SET count = ?
        """
        cursor.execute(query, (json_txt,))
        conn.commit()

        conn.close()
        print(f"Item details saved to database.")
    except Exception as e:
        print("Error inserting data:", e)

