import sqlite3
import os


os.makedirs("NewsStorage", exist_ok=True)

db_name = "NewsStorage/storage.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

columns = ["key TEXT PRIMARY KEY"]
columns += [f"hexaDecValue{i} TEXT" for i in range(1, 51)]
create_table_sql = f"CREATE TABLE IF NOT EXISTS storage ({', '.join(columns)});"

try:
    cursor.execute(create_table_sql)
    conn.commit()
    print("Database created successfully with 50 columns.")
except sqlite3.Error as e:
    print(f"SQL error: {e}")
finally:
    conn.close()
