from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error

app = FastAPI()

# Database connection parameters
DB_HOST = "sql5.freesqldatabase.com"  # e.g., "sql12.freesqldatabase.com"
DB_USER = "sql5766131"  # e.g., "sql1234567"
DB_PASSWORD = "DGa18iw8Xm"  # e.g., "your_password"
DB_NAME = "sql5766131"  # e.g., "sql1234567"

def create_connection():
    """Create a database connection."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Free SQL Database!"}

@app.get("/items/")
def read_items():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")  # Replace with your actual table name
    items = cursor.fetchall()
    cursor.close()
    connection.close()
    return items

@app.get("/items/{item_id}")
def read_item(item_id: int):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))  # Replace with your actual table name
    item = cursor.fetchone()
    cursor.close()
    connection.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item