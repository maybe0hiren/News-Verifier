import sqlite3
import os
from genKeyHexa import createKey, getHexadecimal

database = "NewsStorage/storage.db"

def getKey(image_path):
    try:
        return createKey(image_path)
    except Exception as e:
        print(f"Error calling createKey: {e}")
        return -1

def getHexadecValue(image_path):
    try:
        return getHexadecimal(image_path)
    except Exception as e:
        print(f"Error calling getHexadecimal: {e}")
        return ""

def dbInsertPair(key, hexa_value):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS storage (
            key INTEGER PRIMARY KEY,
            {}
        )
    '''.format(', '.join([f"hexaDecValue{i} TEXT" for i in range(1, 51)])))

    try:
        cursor.execute("INSERT INTO storage (key, hexaDecValue1) VALUES (?, ?)", (key, hexa_value))
        print(f"Key: {key} - Value: {hexa_value} Inserted!")
    except sqlite3.IntegrityError:
        print(f"Insert failed: Key {key} already exists.")
    conn.commit()
    conn.close()

def dbAppendPair(key, hexa_value):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(f"SELECT {', '.join([f'hexaDecValue{i}' for i in range(2, 51)])} FROM storage WHERE key = ?", (key,))
    row = cursor.fetchone()

    if row:
        for i, value in enumerate(row, start=2):
            if value is None:
                column_name = f"hexaDecValue{i}"
                cursor.execute(f"UPDATE storage SET {column_name} = ? WHERE key = ?", (hexa_value, key))
                print(f"Row updated in {column_name}!")
                break
        else:
            print(f"No empty column found for key {key}")
    else:
        print(f"No row found for key {key}")
    
    conn.commit()
    conn.close()

def keyExists(key):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM storage WHERE key = ? LIMIT 1", (key,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


if __name__ == "__main__":
    image_path = "dataset/train/fake/0006.jpg"
    key = getKey(image_path)
    hexadecValue = getHexadecValue(image_path)

    if key == -1 or not hexaDecValue:
        pass

    if keyExists(key):
        dbAppendPair(key, hexaDecValue)
    else:
        dbInsertPair(key, hexaDecValue)
