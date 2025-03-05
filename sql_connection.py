import mysql.connector
from mysql.connector import Error
import pandas as pd

book = pd.read_csv(r"C:\Users\AJAY\Downloads\PROJECT\Capstone_2\dance_book_data.csv")
books_df = pd.DataFrame(book)

# Function to create MySQL connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "Narut0@kurama",
            database = "bookscape"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Function to create the 'dance_book' table
def create_dance_book_data_table():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dance_book_data (
                    book_id VARCHAR(255) PRIMARY KEY,
                    search_key VARCHAR(255),
                    book_title VARCHAR(255),
                    book_subtitle TEXT,
                    book_authors TEXT,
                    book_description TEXT,
                    industry_Identifiers TEXT,
                    text_reading_Modes BOOLEAN,
                    image_reading_Modes BOOLEAN,
                    page_Count INT,
                    categories TEXT,
                    language VARCHAR(10),
                    image_Links TEXT,
                    ratings_Count INT,
                    average_Rating DECIMAL(3, 2),
                    country VARCHAR(10),
                    saleability VARCHAR(50),
                    is_Ebook BOOLEAN,
                    amount_listPrice DECIMAL(10, 2),
                    currencyCode_listPrice VARCHAR(10),
                    amount_retailPrice DECIMAL(10, 2),
                    currencyCode_retailPrice VARCHAR(10),
                    buy_Link TEXT,
                    year VARCHAR(10),
                    publisher TEXT
                )
            """)
            connection.commit()
            print("Table 'dance_book_data' created successfully!")
        except Error as e:
            print(f"Error creating table: {e}")
        finally:
            cursor.close()
            connection.close()

# Create the table
create_dance_book_data_table()

# Function to insert data into MySQL
def insert_books_to_mysql(books_df):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            for _, row in books_df.iterrows():
                cursor.execute("""
    INSERT IGNORE INTO dance_book_data VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
""", tuple(row))
            connection.commit()
            print("Data inserted into MySQL successfully!")
        except Error as e:
            print(f"Error inserting data: {e}")
        finally:
            cursor.close()
            connection.close()

# Insert data into MySQL
insert_books_to_mysql(books_df)


